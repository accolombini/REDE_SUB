'''
    REDE_SUB.py

        ||> Objetivo: o script flexível para incorporar ajustes com base no feedback da equipe e validar os resultados com diferentes cenários.

        ||> Validação com Feedback:
            Permitir a entrada de um arquivo feedback_ajustes.csv contendo os pesos ajustados ou alterações específicas nos parâmetros de criticidade.
            O script irá ler esse arquivo, aplicar os ajustes, e recalcular os valores da matriz de priorização.
            
        ||> Teste de Cenários:
            Implementar uma função para testar diferentes cenários de pesos automaticamente.
            Gerar relatórios comparativos entre os cenários, destacando as discrepâncias e impactos nos rankings.
            
        ||> Mensagem Informativa:
            Adicionar mensagens detalhadas para indicar claramente quais ajustes foram realizados e os impactos observados.
            
        ||> Relatórios Refinados:
            Gerar um relatório final consolidado mostrando o ranking atualizado e os ajustes aplicados.
'''

# Import de bibliotecas

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Funções para manipulação e análise de dados


def create_template(output_path, template_type):
    """
    Gera um arquivo CSV template para diferentes tipos de dados.

    Args:
        output_path (str): Caminho para salvar o arquivo CSV.
        template_type (str): Tipo de template a ser gerado ('campo' ou 'feedback').
    """
    if template_type == 'campo':
        data = {
            "ID_Ativo": ["A001", "A002", "A003"],
            "Medicoes": [0.80, 0.70, 0.60],
            "Observacoes": ["Sem problemas.", "Pequenos ajustes.", "Revisão necessária."]
        }
    elif template_type == 'feedback':
        data = {
            "ID_Ativo": ["A001", "A002"],
            "Frequencia_Falhas": [0.45, 0.35],
            "Impacto_DEC_FEC": [0.75, 0.65],
            "Ponderacao_Total": [0.70, 0.60]
        }
    else:
        raise ValueError("Tipo de template desconhecido.")

    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"Template de {template_type} gerado em: {output_path}")


def calculate_criticidade_matriz(matriz_data, weights):
    """
    Calcula a coluna Criticidade_Matriz com base nas colunas existentes e nos pesos fornecidos.

    Args:
        matriz_data (pd.DataFrame): Dados da matriz de priorização.
        weights (dict): Pesos para cada variável.

    Returns:
        pd.DataFrame: Dados da matriz com a coluna Criticidade_Matriz adicionada.
    """
    matriz_data["Criticidade_Matriz"] = (
        weights["Frequencia_Falhas"] * matriz_data["Frequencia_Falhas"] +
        weights["Impacto_DEC_FEC"] * matriz_data["Impacto_DEC_FEC"] +
        weights["Ponderacao_Total"] * matriz_data["Ponderacao_Total"]
    )
    return matriz_data


def apply_feedback(matriz_data, feedback_path):
    """
    Aplica ajustes na matriz de priorização com base no feedback fornecido.

    Args:
        matriz_data (pd.DataFrame): Dados da matriz de priorização.
        feedback_path (str): Caminho para o arquivo de feedback com ajustes.

    Returns:
        pd.DataFrame: Matriz ajustada.
    """
    if not os.path.exists(feedback_path):
        print("[AVISO] Arquivo de feedback não encontrado. Nenhum ajuste será aplicado.")
        return matriz_data

    feedback = pd.read_csv(feedback_path)
    for index, row in feedback.iterrows():
        if row["ID_Ativo"] in matriz_data["ID_Ativo"].values:
            for col in row.index:
                if col in matriz_data.columns and not pd.isna(row[col]):
                    matriz_data.loc[matriz_data["ID_Ativo"]
                                    == row["ID_Ativo"], col] = row[col]
    print("[SUCESSO] Ajustes de feedback aplicados à matriz de priorização.")
    return matriz_data


def consolidate_data(field_data_path, matriz_data_path, feedback_path, output_path, weights):
    """
    Consolida dados da matriz de priorização com os dados de campo e aplica ajustes de feedback.

    Args:
        field_data_path (str): Caminho para os dados de campo.
        matriz_data_path (str): Caminho para os dados da matriz de priorização.
        feedback_path (str): Caminho para o arquivo de feedback com ajustes.
        output_path (str): Caminho para salvar os dados consolidados.
        weights (dict): Pesos para calcular Criticidade_Matriz.

    Returns:
        pd.DataFrame: Dados consolidados.
    """
    if not os.path.exists(field_data_path):
        print("[AVISO] Arquivo de dados de campo não encontrado. Gerando template...")
        create_template(field_data_path, 'campo')

    if not os.path.exists(matriz_data_path):
        print(
            "[AVISO] Arquivo da matriz de priorização não encontrado. Gerando template...")
        create_template(matriz_data_path, 'feedback')

    # Carregar dados
    field_data = pd.read_csv(field_data_path)
    matriz_data = pd.read_csv(matriz_data_path)

    # Adicionar Criticidade_Matriz se necessário
    if "Criticidade_Matriz" not in matriz_data.columns:
        print("[INFO] Calculando coluna Criticidade_Matriz...")
        matriz_data = calculate_criticidade_matriz(matriz_data, weights)

    # Aplicar ajustes de feedback
    matriz_data = apply_feedback(matriz_data, feedback_path)

    # Consolidar dados
    consolidated = pd.merge(matriz_data, field_data,
                            on="ID_Ativo", how="outer")
    consolidated["Discrepancia"] = abs(
        consolidated["Criticidade_Matriz"] - consolidated["Medicoes"]) / consolidated["Criticidade_Matriz"]
    consolidated["Ajustes_Propostos"] = consolidated["Discrepancia"].apply(
        lambda x: "Reavaliar" if x > 0.1 else "Manter")

    # Salvar dados consolidados
    consolidated.to_csv(output_path, index=False)
    print(f"[SUCESSO] Dados consolidados salvos em: {output_path}")
    return consolidated


def test_scenarios(consolidated_data, weights_list):
    """
    Testa diferentes cenários de pesos e avalia o impacto nos rankings.

    Args:
        consolidated_data (pd.DataFrame): Dados consolidados.
        weights_list (list): Lista de dicionários com diferentes configurações de pesos.

    Returns:
        None
    """
    output_dir = "cenarios"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, weights in enumerate(weights_list):
        print(f"[INFO] Testando cenário {i + 1} com pesos: {weights}")
        scenario_data = calculate_criticidade_matriz(
            consolidated_data.copy(), weights)
        scenario_data = scenario_data.sort_values(
            by="Criticidade_Matriz", ascending=False)
        output_path = os.path.join(output_dir, f"cenario_{i + 1}_rankings.csv")
        scenario_data.to_csv(output_path, index=False)
        print(f"[SUCESSO] Resultados do cenário {
              i + 1} salvos em: {output_path}")


def main():
    """
    Executa o script principal para validação, refinamento e testes de cenários.
    """
    base_path = "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_SUB/script/DADOS"

    # Caminhos para os arquivos
    field_data_path = os.path.join(base_path, "dados_campo.csv")
    matriz_data_path = os.path.join(base_path, "ep3_matriz_priorizacao.csv")
    feedback_path = os.path.join(base_path, "feedback_ajustes.csv")
    consolidated_data_path = os.path.join(base_path, "dados_consolidados.csv")

    # Pesos para o cálculo de Criticidade_Matriz
    weights = {
        "Frequencia_Falhas": 0.4,
        "Impacto_DEC_FEC": 0.4,
        "Ponderacao_Total": 0.2
    }

    # Consolidação de dados com ajustes de feedback
    print("[INFO] Consolidando dados...")
    consolidated_data = consolidate_data(
        field_data_path, matriz_data_path, feedback_path, consolidated_data_path, weights)

    # Teste de cenários
    print("[INFO] Testando diferentes cenários de pesos...")
    scenarios = [
        {"Frequencia_Falhas": 0.3, "Impacto_DEC_FEC": 0.5, "Ponderacao_Total": 0.2},
        {"Frequencia_Falhas": 0.5, "Impacto_DEC_FEC": 0.3, "Ponderacao_Total": 0.2},
        {"Frequencia_Falhas": 0.4, "Impacto_DEC_FEC": 0.4, "Ponderacao_Total": 0.2}
    ]
    test_scenarios(consolidated_data, scenarios)


if __name__ == "__main__":
    main()
