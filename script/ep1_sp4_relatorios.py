'''
    REDE_SUB

        ||> Geração Automática de Relatórios em PDF:
                Utilizar a biblioteca ReportLab ou PDFKit para consolidar os dados em um relatório formatado.
                Incluir tabelas, gráficos e explicações das análises realizadas em cada sprint.
            
            |> Exportação de Resultados Consolidados:
                Criar um arquivo Excel consolidado utilizando o pandas e o XlsxWriter.
                Cada aba pode conter os resultados de uma sprint:
                Sprint 1: Análise exploratória inicial.
                Sprint 2: Resultados das simulações.
                Sprint 3: Modelos refinados e resultados ajustados.
            
            |> Sumarização do Processo:
                Criar uma função para gerar um resumo detalhado das etapas realizadas e resultados principais.
                Este resumo pode ser exportado como texto simples ou markdown para facilitar a inclusão em relatórios.
            
            |> Visualizações Dinâmicas para Apresentação:
                Gerar apresentações utilizando Plotly para criar gráficos interativos que possam ser exibidos diretamente no workshop final.

        ||> Resultados Esperados
                Relatório Final em PDF contendo:
                Introdução e objetivos.
                Resultados consolidados das sprints.
                Visualizações dos ativos mais críticos.
                Arquivo Excel Consolidado com todas as análises e dados exportados para revisões futuras.
                Preparação para Apresentações com gráficos interativos.
'''

# Import de bibliotecas

import pandas as pd
from fpdf import FPDF
import plotly.express as px
import os

# Definir caminhos para os dados e saídas
data_path = os.path.join(
    "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_SUB/script/DADOS",
    "historico_light.csv"
)
output_pdf_path = os.path.join(
    "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_SUB/script/DADOS",
    "relatorio_final_completo.pdf"
)
output_excel_path = os.path.join(
    "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_SUB/script/DADOS",
    "dados_consolidados.xlsx"
)


def ensure_directory_exists(directory):
    """
    Verifica se o diretório existe e o cria se não existir.

    Args:
        directory (str): Caminho do diretório a ser verificado/criado.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


# Garante que o diretório de saída existe
ensure_directory_exists(
    "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_SUB/script/DADOS"
)


class PDFReport(FPDF):
    """
    Classe para criar relatórios PDF formatados com cabeçalhos, capítulos e gráficos.
    """

    def header(self):
        """Adiciona o cabeçalho ao PDF."""
        self.set_font('Arial', 'B', 12)
        self.cell(
            0, 10, 'Relatório Final - Critérios de Classificação da Criticidade', 0, 1, 'C')
        self.ln(10)

    def chapter_title(self, chapter_title):
        """Adiciona um título de capítulo ao PDF."""
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, chapter_title, 0, 1, 'L')
        self.ln(8)

    def chapter_body(self, body):
        """Adiciona o corpo do capítulo ao PDF."""
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln(5)

    def add_chart(self, figure, chart_title):
        """
        Adiciona um gráfico ao PDF.

        Args:
            figure: Figura gerada com Plotly para ser adicionada ao PDF.
            chart_title: Título do gráfico a ser adicionado no relatório.
        """
        self.add_page()
        self.chapter_title(chart_title)
        self.ln(15)  # Espaço antes do gráfico
        temp_chart_path = os.path.join(
            "/Users/accol/Library Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_SUB/script/DADOS",
            "temp_chart.png"
        )
        figure.write_image(temp_chart_path)  # Salvar o gráfico como imagem
        # Ajustar posicionamento para evitar sobreposição
        self.image(temp_chart_path, x=10, y=60, w=180)
        self.ln(120)  # Espaço após o gráfico
        # Remover o arquivo temporário após uso
        os.remove(temp_chart_path)


# Verifica se o arquivo de dados existe
if not os.path.exists(data_path):
    raise FileNotFoundError(
        f"Arquivo de dados não encontrado no caminho: {data_path}")

# Carregar os dados do arquivo CSV
df = pd.read_csv(data_path)

# Instanciar o relatório PDF
pdf = PDFReport()
pdf.add_page()

# Adicionar introdução ao relatório
pdf.chapter_title("Introdução")
pdf.chapter_body(
    """
    Este relatório apresenta os resultados consolidados do projeto, abrangendo:
    - Objetivos do projeto e metodologia aplicada.
    - Resultados obtidos em cada sprint.
    - Visualizações e dados de apoio para priorização e tomada de decisão.
    """
)

# Adicionar análise exploratória (Sprint 1)
pdf.chapter_title("Sprint 1: Análise Exploratória")
pdf.chapter_body(
    """
    A análise exploratória identificou as principais variáveis e características dos ativos de 
    média tensão da rede subterrânea, com foco na frequência de falhas, tempo de operação, 
    impacto DEC/FEC e número de clientes afetados.
    """
)
top_ativos = df.sort_values("Impacto_DEC_FEC", ascending=False).head(10)
fig1 = px.bar(
    top_ativos,
    x="ID_Ativo",
    y="Impacto_DEC_FEC",
    title="Ativos com Maior Impacto DEC/FEC"
)
pdf.add_chart(fig1, "Gráfico: Ativos com Maior Impacto DEC/FEC")

# Adicionar modelo inicial de criticidade (Sprint 2)
pdf.chapter_title("Sprint 2: Modelo Inicial de Criticidade")
pdf.chapter_body(
    """
    Um modelo preliminar de criticidade foi desenvolvido, considerando pesos ajustáveis para as 
    variáveis frequência de falhas e impacto DEC/FEC. Cenários foram simulados para validar a robustez.
    """
)

# Adicionar validação e ajustes (Sprint 3)
pdf.chapter_title("Sprint 3: Validação e Ajustes")
pdf.chapter_body(
    """
    Os resultados das validações técnicas ajustaram os pesos para refletir a realidade operacional. 
    O modelo foi refinado e priorizou os ativos com maior criticidade.
    """
)
fig2 = px.bar(
    top_ativos,
    x="ID_Ativo",
    y="Impacto_DEC_FEC",
    title="Ativos Mais Críticos Após Ajuste de Pesos"
)
pdf.add_chart(fig2, "Gráfico: Ativos Mais Críticos")

# Salvar o PDF na pasta de saída
pdf.output(output_pdf_path)

# Exportar dados consolidados para um arquivo Excel
try:
    with pd.ExcelWriter(output_excel_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Dados Originais', index=False)
        top_ativos.to_excel(writer, sheet_name='Ativos Críticos', index=False)
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "A biblioteca 'xlsxwriter' não foi encontrada. Instale-a com 'pip install xlsxwriter'.")

# Exibir mensagens de sucesso
print(f"Relatório PDF salvo em: {output_pdf_path}")
print(f"Arquivo Excel salvo em: {output_excel_path}")
