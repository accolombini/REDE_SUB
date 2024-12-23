'''
    REDE_SUB.docx

        ||> Objetivo: concentra em integrar os dados de campo à matriz existente, revisando e ajustando-a com base nas novas informações.

        ||> Integração e revisão da matriz:
            Adicionar lógica para ajustar os pesos das variáveis com base em novos dados.
            Permitir que a consolidação inclua variáveis adicionais provenientes das inspeções.
            
        ||> Implementar ajustes iniciais:
            Introduzir flexibilidade no cálculo de Criticidade_Matriz, permitindo ajustes nos pesos de forma dinâmica.
            
        ||> Geração da matriz revisada:
            Salvar a matriz revisada com os dados integrados e ajustes aplicados.

'''

# Import de bibliotecas

import os
import pandas as pd
from fpdf import FPDF

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
        print("Arquivo de dados de campo não encontrado. Gerando template...")
        create_field_data_template(field_data_path)

    if not os.path.exists(matriz_data_path):
        print("Arquivo da matriz de priorização não encontrado. Gerando template...")
        create_matriz_priorizacao_template(matriz_data_path)

    # Carregar dados
    field_data = pd.read_csv(field_data_path)
    matriz_data = pd.read_csv(matriz_data_path)

    # Adicionar Criticidade_Matriz se necessário
    if "Criticidade_Matriz" not in matriz_data.columns:
        print("Calculando coluna Criticidade_Matriz...")
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
    print(f"Dados consolidados salvos em: {output_path}")
    return consolidated


def generate_final_report(output_path, consolidated_data):
    """
    Gera um relatório final consolidado em PDF.

    Args:
        output_path (str): Caminho para salvar o relatório em PDF.
        consolidated_data (pd.DataFrame): Dados consolidados para o relatório.
    """
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=16, style="B")
    pdf.cell(200, 10, txt="Relatório Final de Inspeções", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.cell(
        0, 10, txt="Consolidação de Dados de Campo e Matriz de Prioridade", ln=True)
    pdf.ln(5)

    # Adicionar dados consolidados
    for index, row in consolidated_data.iterrows():
        pdf.cell(0, 10, txt=f"Ativo {row['ID_Ativo']}: Criticidade Matriz = {row['Criticidade_Matriz']:.2f}, "
                 f"Criticidade Campo = {row['Medicoes']}, Discrepância = {
                     row['Discrepancia']:.2f}, "
                 f"Ajuste = {row['Ajustes_Propostos']}", ln=True)
        pdf.ln(5)

    pdf.output(output_path)
    print(f"Relatório final gerado em: {output_path}")


def main():
    """
    Executa o script principal para consolidação e análise de resultados.
    """
    base_path = "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_SUB/script/DADOS"

    # Caminhos para os arquivos
    field_data_path = os.path.join(base_path, "dados_campo.csv")
    matriz_data_path = os.path.join(base_path, "ep3_matriz_priorizacao.csv")
    consolidated_data_path = os.path.join(base_path, "dados_consolidados.csv")
    final_report_path = os.path.join(
        base_path, "relatorio_final_inspecoes.pdf")

    # Pesos para o cálculo de Criticidade_Matriz
    weights = {
        "Frequencia_Falhas": 0.4,
        "Impacto_DEC_FEC": 0.4,
        "Ponderacao_Total": 0.2
    }

    # Consolidação de dados
    print("Consolidando dados...")
    consolidated_data = consolidate_data(
        field_data_path, matriz_data_path, consolidated_data_path, weights)

    # Geração do relatório final
    print("Gerando relatório final...")
    generate_final_report(final_report_path, consolidated_data)


if __name__ == "__main__":
    main()
