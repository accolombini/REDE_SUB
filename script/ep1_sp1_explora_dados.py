'''
    REDE_SUB

    |> Objetivo:
        ||> Revisar e explorar os dados para identificar variáveis relevantes, como: 
            Frequência de falhas.
            Tempo de operação.
            Impacto nos indicadores regulatórios (DEC e FEC).
            Número de clientes afetados.
            Detectar possíveis lacunas nos dados e verificar consistência.
            Gerar visualizações iniciais para apoiar a interpretação dos dados.
'''

import pandas as pd
import numpy as np
import missingno as msno
import plotly.express as px
import matplotlib.pyplot as plt  # Usado apenas para salvar gráficos do missingno

# **Docstring principal do script**
"""
Este script realiza a análise exploratória inicial da base de dados de ativos subterrâneos.
Inclui verificações de valores ausentes, cálculo de estatísticas descritivas, análise de correlações e visualizações de distribuições.
Os resultados ajudam a identificar variáveis relevantes e validar a qualidade dos dados.
"""

# Caminho do arquivo de dados
data_path = "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_SUB/script/DADOS/historico_light.csv"

# Carregamento dos dados
df = pd.read_csv(data_path)
print("Dados carregados com sucesso.")

# **Resumo Estatístico**
print("Resumo Estatístico:\n", df.describe())
print("\nTipos de Dados:\n", df.dtypes)

# **Verificação de Valores Ausentes**
"""
Visualiza e salva a matriz de valores ausentes, indicando onde podem existir lacunas nos dados.
"""
print("\nVerificando valores ausentes:")
print(df.isnull().sum())

# Gerar gráfico de valores ausentes com Missingno
plt.figure(figsize=(10, 6))
msno.matrix(df)
plt.title("Matriz de Valores Ausentes")
missingno_output_path = "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_SUB/script/DADOS/missingno_matrix.png"
plt.savefig(missingno_output_path, dpi=300)  # Salva o gráfico como PNG
plt.close()
print(f"Matriz de valores ausentes salva em: {missingno_output_path}")

# **Análise de Correlações**
"""
Calcula a matriz de correlação para variáveis numéricas e a visualiza usando um mapa de calor interativo.
"""
correlation_matrix = df.corr(
    numeric_only=True)  # Calcula correlações numéricas
print("\nMatriz de Correlações:\n", correlation_matrix)

# Visualizar correlações com Plotly
fig = px.imshow(
    correlation_matrix,
    title="Matriz de Correlação",
    labels=dict(color="Correlação"),
    color_continuous_scale="RdBu",  # Escala de cores suportada pelo Plotly
    text_auto=".2f"
)
fig.show()

# **Distribuições das Variáveis**
"""
Plota histogramas interativos para variáveis-chave, ajudando a entender suas distribuições.
"""
for col in ["Frequencia_Falhas", "Tempo_Operacao", "Impacto_DEC_FEC", "Numero_Clientes_Afetados"]:
    fig = px.histogram(
        df,
        x=col,
        nbins=20,
        title=f"Distribuição de {col}",
        labels={col: col, "count": "Frequência"},
        template="plotly_white"
    )
    fig.show()

# **Análise por Tipo de Ativo**
"""
Calcula e visualiza o impacto médio de DEC/FEC por tipo de ativo.
"""
impacto_por_tipo = df.groupby("Tipo_Ativo")[
    "Impacto_DEC_FEC"].mean().sort_values(ascending=False)
print("\nImpacto DEC/FEC Médio por Tipo de Ativo:\n", impacto_por_tipo)

# Visualizar impacto DEC/FEC por tipo de ativo com Plotly
fig = px.bar(
    impacto_por_tipo,
    x=impacto_por_tipo.index,
    y=impacto_por_tipo.values,
    title="Impacto Médio DEC/FEC por Tipo de Ativo",
    labels={"x": "Tipo de Ativo", "y": "Impacto DEC/FEC Médio"},
    template="plotly_white"
)
fig.show()

# **Análise Temporal**
"""
Verifica a consistência das datas no conjunto de dados e plota a distribuição de eventos por ano.
"""
df["Data_Evento"] = pd.to_datetime(df["Data_Evento"])  # Converte para datetime
print("\nDatas mais recentes:", df["Data_Evento"].max())
print("Datas mais antigas:", df["Data_Evento"].min())

# Plotar distribuição de eventos por ano
df["Ano_Evento"] = df["Data_Evento"].dt.year
fig = px.histogram(
    df,
    x="Ano_Evento",
    title="Distribuição de Eventos por Ano",
    labels={"Ano_Evento": "Ano", "count": "Número de Eventos"},
    template="plotly_white"
)
fig.show()

# **Exportação dos Resultados**
"""
Exporta um resumo descritivo completo para um arquivo CSV para consulta futura.
"""
output_path = "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_SUB/script/DADOS/analise_exploratoria_inicial.csv"
df.describe(include="all").to_csv(output_path)
print(f"Análise exploratória inicial exportada para: {output_path}")
