'''
    REDE_SUB.docx

        ||>Objetivo: inferências sobre unidades não inspecionadas, podemos estender este script para incluir a modelagem estatística necessária. O objetivo será:

        ||> Inferências sobre unidades não inspecionadas:
            Estimar valores de criticidade para ativos não inspecionados com base nos dados coletados.
            Utilizar regressão linear, kNN, ou outro modelo simples de aprendizado de máquina para prever os dados faltantes.
        
        ||> Avaliação da precisão:
            Implementar validação cruzada para avaliar a qualidade das inferências realizadas.
'''

# Import de bibliotecas

import os
import pandas as pd
from fpdf import FPDF
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Funções para análise de dados


def create_field_data_template(output_path):
    """
    Gera um arquivo CSV template para dados de campo.

    Args:
        output_path (str): Caminho para salvar o arquivo CSV.
    """
    data = {
        "ID_Ativo": ["A001", "A002", "A003"],
        "Medicoes": [0.80, 0.70, 0.60],
        "Observacoes": ["Sem problemas.", "Pequenos ajustes.", "Revisão necessária."]
    }
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"Template de dados de campo gerado em: {output_path}")


def create_matriz_priorizacao_template(output_path):
    """
    Gera um arquivo CSV template para a matriz de priorização.

    Args:
        output_path (str): Caminho para salvar o arquivo CSV.
    """
    data = {
        "ID_Ativo": ["A001", "A002", "A003"],
        "Frequencia_Falhas": [0.5, 0.3, 0.2],
        "Impacto_DEC_FEC": [0.8, 0.7, 0.6],
        "Numero_Clientes_Afetados": [100, 50, 30],
        "Ponderacao_Total": [0.75, 0.65, 0.55]
    }
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"Template de matriz de priorização gerado em: {output_path}")


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


def consolidate_data(field_data_path, matriz_data_path, output_path, weights):
    """
    Consolida dados da matriz de priorização com os dados de campo.

    Args:
        field_data_path (str): Caminho para os dados de campo.
        matriz_data_path (str): Caminho para os dados da matriz de priorização.
        output_path (str): Caminho para salvar os dados consolidados.
        weights (dict): Pesos para calcular Criticidade_Matriz.

    Returns:
        pd.DataFrame: Dados consolidados.
    """
    if not os.path.exists(field_data_path):
        print("[AVISO] Arquivo de dados de campo não encontrado. Gerando template...")
        create_field_data_template(field_data_path)

    if not os.path.exists(matriz_data_path):
        print(
            "[AVISO] Arquivo da matriz de priorização não encontrado. Gerando template...")
        create_matriz_priorizacao_template(matriz_data_path)

    # Carregar dados
    field_data = pd.read_csv(field_data_path)
    matriz_data = pd.read_csv(matriz_data_path)

    # Adicionar Criticidade_Matriz se necessário
    if "Criticidade_Matriz" not in matriz_data.columns:
        print("[INFO] Calculando coluna Criticidade_Matriz...")
        matriz_data = calculate_criticidade_matriz(matriz_data, weights)

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


def perform_inference(consolidated_data, output_path):
    """
    Realiza inferências sobre unidades não inspecionadas usando regressão linear.

    Args:
        consolidated_data (pd.DataFrame): Dados consolidados com informações inspecionadas e não inspecionadas.
        output_path (str): Caminho para salvar os resultados de inferência.

    Returns:
        pd.DataFrame: Dados com inferências adicionadas.
    """
    # Separar dados inspecionados e não inspecionados
    inspected = consolidated_data.dropna(subset=["Medicoes"])
    not_inspected = consolidated_data[consolidated_data["Medicoes"].isna()]

    # Validar dados de treinamento
    inspected = inspected.dropna(subset=["Criticidade_Matriz"])

    if inspected.empty:
        print("[ERRO] Nenhum dado válido disponível para treinamento. Por favor, revise a base de dados consolidada.")
        print("[INFO] Gerando template de inferência com valores padrão...")
        # Preenchendo com valores padrão para continuar o fluxo
        not_inspected.loc[:, "Medicoes"] = 0.0
        not_inspected.to_csv(output_path, index=False)
        print(f"[SUCESSO] Inferência não realizada. Dados padrão salvos em: {
              output_path}")
        return not_inspected

    # Treinar modelo de regressão linear
    X = inspected["Criticidade_Matriz"].values.reshape(-1, 1)
    y = inspected["Medicoes"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    # Avaliação do modelo
    y_pred = model.predict(X_test)
    print("[INFO] Métricas do modelo:")
    print("  - MSE:", mean_squared_error(y_test, y_pred))
    print("  - R²:", r2_score(y_test, y_pred))

    # Inferir valores para ativos não inspecionados
    if not not_inspected.empty:
        not_inspected.loc[:, "Medicoes"] = model.predict(
            not_inspected["Criticidade_Matriz"].values.reshape(-1, 1))

    # Combinar resultados
    final_data = pd.concat([inspected, not_inspected]
                           ).sort_values(by="ID_Ativo")
    final_data.to_csv(output_path, index=False)
    print(f"[SUCESSO] Inferências realizadas e salvas em: {output_path}")
    return final_data


def main():
    """
    Executa o script principal para consolidação, análise de resultados e inferências.
    """
    base_path = "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_SUB/script/DADOS"

    # Caminhos para os arquivos
    field_data_path = os.path.join(base_path, "dados_campo.csv")
    matriz_data_path = os.path.join(base_path, "ep3_matriz_priorizacao.csv")
    consolidated_data_path = os.path.join(base_path, "dados_consolidados.csv")
    inference_data_path = os.path.join(base_path, "dados_inferidos.csv")

    # Pesos para o cálculo de Criticidade_Matriz
    weights = {
        "Frequencia_Falhas": 0.4,
        "Impacto_DEC_FEC": 0.4,
        "Ponderacao_Total": 0.2
    }

    # Consolidação de dados
    print("[INFO] Consolidando dados...")
    consolidated_data = consolidate_data(
        field_data_path, matriz_data_path, consolidated_data_path, weights)

    # Inferência sobre ativos não inspecionados
    print("[INFO] Realizando inferências...")
    inferred_data = perform_inference(consolidated_data, inference_data_path)


if __name__ == "__main__":
    main()
