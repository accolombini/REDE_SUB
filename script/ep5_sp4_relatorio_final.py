'''
    REDE_SUB.docx

        ||> Objetivo: consolida todos os dados relevantes do projeto e gera um relatório final em PDF, incluindo análises e resultados.


'''

# Import de bibliotecas

import os
from fpdf import FPDF
import pandas as pd

# Funções para geração de relatórios


def consolidate_all_data(base_path, consolidated_path):
    """
    Consolida todos os dados relevantes ao longo do projeto em um único DataFrame.

    Args:
        base_path (str): Caminho base para os arquivos gerados ao longo do projeto.
        consolidated_path (str): Caminho para salvar os dados consolidados finais.

    Returns:
        pd.DataFrame: Dados consolidados finais.
    """
    print("[INFO] Consolidando todos os dados...")

    # Lista de arquivos esperados
    files = [
        os.path.join(base_path, "dados_campo.csv"),
        os.path.join(base_path, "ep3_matriz_priorizacao.csv"),
        os.path.join(base_path, "dados_consolidados.csv"),
        os.path.join(base_path, "feedback_ajustes.csv")
    ]

    # Verificar existência dos arquivos
    dataframes = []
    for file in files:
        if os.path.exists(file):
            print(f"[SUCESSO] Arquivo encontrado: {file}")
            df = pd.read_csv(file)
            df["Fonte"] = os.path.basename(file)
            dataframes.append(df)
        else:
            print(f"[AVISO] Arquivo não encontrado: {file}")

    # Consolidar todos os DataFrames
    consolidated_data = pd.concat(dataframes, ignore_index=True)
    consolidated_data.to_csv(consolidated_path, index=False)
    print(f"[SUCESSO] Dados consolidados finais salvos em: {
          consolidated_path}")

    return consolidated_data


def generate_final_report(consolidated_data, output_path):
    """
    Gera o relatório final em PDF com base nos dados consolidados.

    Args:
        consolidated_data (pd.DataFrame): Dados consolidados finais.
        output_path (str): Caminho para salvar o relatório PDF.
    """
    print("[INFO] Gerando relatório final...")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Título
    pdf.set_font("Arial", size=14, style="B")
    pdf.cell(200, 10, txt="Relatório Final do Projeto", ln=True, align="C")
    pdf.ln(10)

    # Resumo
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(
        0, 10, txt="Este relatório apresenta os resultados consolidados do projeto, incluindo as principais conclusões, produtos e recomendações.")
    pdf.ln(10)

    # Principais métricas
    pdf.set_font("Arial", size=12, style="B")
    pdf.cell(200, 10, txt="Principais Resultados Consolidado", ln=True)

    pdf.set_font("Arial", size=10)
    for col in consolidated_data.columns:
        pdf.cell(0, 10, txt=f"- {col}", ln=True)
    pdf.ln(10)

    # Adicionar tabela com resumo de dados
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Resumo Consolidado de Dados", ln=True)
    pdf.ln(5)

    columns = consolidated_data.columns
    for i in range(min(10, len(consolidated_data))):  # Limitar a 10 linhas para visualização
        row = consolidated_data.iloc[i]
        row_text = " | ".join([f"{col}: {row[col]}" for col in columns])
        pdf.multi_cell(0, 10, txt=row_text)
        pdf.ln(2)

    # Salvar o relatório
    pdf.output(output_path)
    print(f"[SUCESSO] Relatório final gerado em: {output_path}")


def main():
    """
    Executa o script principal para consolidação e geração do relatório final.
    """
    base_path = "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_SUB/script/DADOS"

    # Caminhos para os arquivos
    consolidated_path = os.path.join(
        base_path, "dados_finais_consolidados.csv")
    report_path = os.path.join(base_path, "relatorio_final_projeto.pdf")

    # Consolidação dos dados
    consolidated_data = consolidate_all_data(base_path, consolidated_path)

    # Geração do relatório final
    generate_final_report(consolidated_data, report_path)


if __name__ == "__main__":
    main()
