''' 
    REDE_SUB.py

    ||> Objetivo: consolidar todos os resultados obtidos até agora em um relatório técnico detalhado. Esse relatório incluirá:

        ||> Descrição Metodológica:
            Explicação do processo para construir a matriz de priorização.
            Detalhamento dos critérios, pesos e variáveis utilizados.
            
            |> Resultados Consolidados:
                Ranking final de criticidade.
                Gráficos relevantes para interpretação, como o ranking e o scatter plot.
                Discussão e Conclusões:

            |> Observações importantes com base nos resultados.
                Sugestões para priorização dos ativos mais críticos.
                Preparação para Apresentação:
                Relatório formatado em PDF ou outro formato de fácil leitura.

        ||> Metodologia Documentada:
            Incluir a descrição do processo de construção e validação da matriz de priorização.
            Resultados Consolidados:
            Listar os 10 ativos mais críticos.
            Inserir gráficos relevantes (ranking e scatter plot) diretamente no relatório.
            
        ||> Conclusões e Recomendações:
            Apresenta observações baseadas nos resultados e sugere próximos passos.
'''

# Import de bibliotecas

import pandas as pd
import plotly.express as px
from fpdf import FPDF
import os

# Funções Utilitárias


def load_normalized_data(file_path):
    """
    Carrega a base de dados normalizada a partir de um arquivo CSV.

    Args:
        file_path (str): Caminho para o arquivo CSV com os dados normalizados.

    Returns:
        pd.DataFrame: DataFrame com os dados normalizados.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    return pd.read_csv(file_path)


def calculate_criticality(df, weights):
    """
    Calcula a criticidade com base nos pesos e variáveis fornecidos.

    Args:
        df (pd.DataFrame): DataFrame com as variáveis normalizadas.
        weights (dict): Dicionário contendo os pesos de cada variável.

    Returns:
        pd.DataFrame: DataFrame atualizado com a coluna de criticidade.
    """
    df['Criticidade'] = sum(df[var] * weight for var,
                            weight in weights.items())
    return df


def save_criticality_matrix(df, output_path):
    """
    Salva a matriz de criticidade em um arquivo CSV.

    Args:
        df (pd.DataFrame): DataFrame contendo a matriz de criticidade.
        output_path (str): Caminho para salvar o arquivo CSV.
    """
    df.to_csv(output_path, index=False)
    print(f"Matriz de priorização salva em: {output_path}")


def generate_pdf_report(df, output_path):
    """
    Gera um relatório técnico em PDF com base nos resultados da matriz de priorização.

    Args:
        df (pd.DataFrame): DataFrame com os resultados da matriz de priorização.
        output_path (str): Caminho para salvar o relatório em PDF.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Título
    pdf.set_font("Arial", size=16, style="B")
    pdf.cell(200, 10, txt="Relatório Final: Matriz de Priorização",
             ln=True, align="C")
    pdf.ln(10)

    # Metodologia
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="""
Este relatório apresenta os resultados da Matriz de Priorização dos Ativos Subterrâneos. 
Foram utilizados critérios definidos em conjunto com a equipe técnica e aplicados pesos para as variáveis-chave:

- Frequência de Falhas
- Tempo de Operação
- Número de Clientes Afetados
- Impacto DEC/FEC

Os dados foram normalizados e ponderados para garantir comparabilidade e objetividade no ranking de criticidade.
    """)
    pdf.ln(5)

    # Resultados Consolidados
    pdf.set_font("Arial", size=14, style="B")
    pdf.cell(0, 10, txt="Resultados Consolidados", ln=True)
    pdf.ln(5)

    # Ranking Final
    pdf.set_font("Arial", size=12)
    top_10 = df.nlargest(10, "Criticidade")
    pdf.cell(0, 10, txt="Top 10 Ativos Críticos:", ln=True)
    for index, row in top_10.iterrows():
        pdf.cell(0, 10, txt=f"- Ativo: {row['ID_Ativo']
                                        } | Criticidade: {row['Criticidade']:.2f}", ln=True)
    pdf.ln(10)

    # Gráficos
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt="Gráficos Relevantes:", ln=True)
    pdf.ln(5)

    # Gerar gráficos temporários
    bar_chart = px.bar(
        df,
        x="Criticidade",
        y="ID_Ativo",
        orientation="h",
        title="Ranking de Criticidade dos Ativos",
        labels={"ID_Ativo": "Ativo", "Criticidade": "Índice de Criticidade"},
    ).update_layout(yaxis={'categoryorder': 'total ascending'})
    scatter_chart = px.scatter(
        df,
        x="Criticidade",
        y="Frequencia_Falhas",
        size="Numero_Clientes_Afetados",
        color="Impacto_DEC_FEC",
        title="Relação entre Criticidade e Variáveis",
        labels={"Frequencia_Falhas": "Frequência de Falhas",
                "Criticidade": "Índice de Criticidade"},
    )

    bar_chart_path = "bar_chart.png"
    scatter_chart_path = "scatter_chart.png"
    bar_chart.write_image(bar_chart_path)
    scatter_chart.write_image(scatter_chart_path)

    pdf.add_page()
    pdf.cell(0, 10, txt="Ranking de Criticidade dos Ativos:", ln=True)
    pdf.image(bar_chart_path, x=10, y=30, w=180)

    pdf.add_page()
    pdf.cell(0, 10, txt="Relação entre Criticidade e Variáveis:", ln=True)
    pdf.image(scatter_chart_path, x=10, y=30, w=180)

    # Conclusão
    pdf.add_page()
    pdf.set_font("Arial", size=14, style="B")
    pdf.cell(0, 10, txt="Conclusões e Recomendações", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="""
Com base nos resultados, recomenda-se priorizar os ativos com maior criticidade para manutenção ou substituição.
As variáveis-chave indicam a importância de considerar tanto o impacto operacional quanto o regulatório para maximizar a eficiência das intervenções.

Próximos passos incluem validação contínua com dados futuros e ajustes no modelo, conforme necessário.
    """)

    # Salvar PDF
    pdf.output(output_path)
    print(f"Relatório salvo em: {output_path}")


# Configurações de Caminhos
base_path = "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_SUB/script/DADOS"
input_path = os.path.join(base_path, "matriz_priorizacao.csv")
output_pdf_path = os.path.join(base_path, "relatorio_final_priorizacao.pdf")

# Pesos para cálculo da criticidade (apenas para referência)
weights = {
    "Frequencia_Falhas": 0.4,
    "Tempo_Operacao": 0.3,
    "Numero_Clientes_Afetados": 0.2,
    "Impacto_DEC_FEC": 0.1
}

# Garantir que o arquivo de matriz exista
if not os.path.exists(input_path):
    print("Matriz de priorização não encontrada. Gerando matriz...")
    normalized_data_path = os.path.join(base_path, "ep3_base_normalizada.csv")
    df_normalized = load_normalized_data(normalized_data_path)
    df_criticality = calculate_criticality(df_normalized, weights)
    save_criticality_matrix(df_criticality, input_path)

# Carregar os dados da matriz de priorização
print("Carregando dados da matriz de priorização...")
df = load_normalized_data(input_path)

# Gerar o relatório
print("Gerando relatório final...")
generate_pdf_report(df, output_pdf_path)
