''' 
    REDE_SUB

    ||> Objetivo:
        Estatísticas descritivas: Resumo das variáveis numéricas.
        Análises gráficas:
        Histogramas para distribuição de variáveis numéricas.
        Boxplots para detecção de outliers.
        Matriz de correlação para explorar relações entre variáveis.
        Geração de relatório em PDF com os gráficos e insights.

            |> Explorar padrões e relações relevantes usando análises estatísticas e correlações.
            |> Detectar outliers e anomalias com base em critérios estatísticos ou gráficos.
            |> Gerar gráficos interativos com Dash/Plotly para facilitar a visualização.
            |> Consolidar insights preliminares em um relatório simples.

            |> O nome do arquivo de saída consolidado será algo como ep2_relatorio_exploratorio.pdf. Vou preparar um script Python com as seguintes funcionalidades:

                Leitura da base tratada (e.g., ep2_base_tratada.csv).
                Criação de gráficos interativos (e.g., histogramas, boxplots e correlações).
                Geração do relatório preliminar.
'''

# Import bibliotecas

import pandas as pd
import plotly.express as px
from fpdf import FPDF
import os

# Definir o caminho da base de dados tratada
base_path = "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_SUB/script/DADOS"
data_path = os.path.join(base_path, "ep2_dados_tratados.csv")
output_pdf_path = os.path.join(base_path, "ep2_relatorio_exploratorio.pdf")

# Classe para geração de relatórios PDF


class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Relatório Preliminar de Análise Exploratória', 0, 1, 'C')
        self.ln(10)

    def chapter_title(self, chapter_title: str):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, chapter_title, 0, 1, 'L')
        self.ln(8)

    def chapter_body(self, body: str):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln(5)

    def add_chart(self, figure, chart_title: str):
        temp_chart_path = os.path.join(base_path, "temp_chart.png")
        figure.write_image(temp_chart_path)
        self.add_page()
        self.chapter_title(chart_title)
        self.image(temp_chart_path, x=10, y=60, w=180)
        os.remove(temp_chart_path)


# Verificar se o arquivo existe
if not os.path.exists(data_path):
    raise FileNotFoundError(f"Arquivo de dados não encontrado: {data_path}")

# Carregar a base de dados tratada
df = pd.read_csv(data_path)

# Filtrar colunas numéricas
numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns

if numerical_columns.empty:
    raise ValueError(
        "A base de dados não contém colunas numéricas para análise exploratória.")

# Instanciar o PDF
pdf = PDFReport()
pdf.add_page()

# Introdução ao relatório
pdf.chapter_title("Introdução")
pdf.chapter_body(
    """
    Este relatório apresenta uma análise exploratória inicial dos dados tratados.
    Ele inclui estatísticas descritivas, gráficos para distribuição das variáveis,
    detecção de outliers e uma matriz de correlação.
    """
)

# Estatísticas descritivas
pdf.chapter_title("Estatísticas Descritivas")
summary = df[numerical_columns].describe()
pdf.chapter_body(summary.to_string())

# Histogramas
pdf.chapter_title("Distribuição das Variáveis")
for column in numerical_columns:
    fig = px.histogram(df, x=column, title=f"Distribuição: {column}")
    pdf.add_chart(fig, f"Distribuição: {column}")

# Boxplots
pdf.chapter_title("Detecção de Outliers")
for column in numerical_columns:
    fig = px.box(df, y=column, title=f"Outliers: {column}")
    pdf.add_chart(fig, f"Outliers: {column}")

# Matriz de correlação
pdf.chapter_title("Matriz de Correlação")
correlation_matrix = df[numerical_columns].corr()
fig = px.imshow(correlation_matrix,
                title="Matriz de Correlação", text_auto=True)
pdf.add_chart(fig, "Matriz de Correlação")

# Salvar relatório
pdf.output(output_pdf_path)
print(f"Relatório salvo em: {output_pdf_path}")
