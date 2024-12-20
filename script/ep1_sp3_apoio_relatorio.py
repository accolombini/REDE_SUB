'''
    REDE_SUB

        ||> Validação Automática de Pesos e Variáveis:
            Durante os workshops técnicos, podemos criar um script para validar automaticamente os pesos sugeridos pelos especialistas, verificando como afetam os resultados finais.
            Python pode recalcular as pontuações de criticidade e identificar discrepâncias com base nas sugestões.
        
        ||> Simulações Adicionais:
            Podemos criar novos cenários rapidamente e testar os resultados em tempo real durante as sessões de validação.
            Isso permite demonstrar de forma visual como os ajustes nos pesos e variáveis impactam a classificação dos ativos.
        
        ||> Refinamento do Modelo:
            Após receber o feedback dos especialistas, Python pode ser usado para ajustar o modelo de criticidade e realizar análises adicionais, como:
            Verificar a estabilidade do modelo.
            Detectar possíveis "outliers" que sejam incoerentes com os critérios ajustados.
        
        ||> Dashboard Interativo:
            Criar um dashboard simples com Plotly Dash para que os especialistas possam interagir com os dados e ajustar pesos em tempo real durante o workshop.
'''

# -*- coding: utf-8 -*-
"""
Script: ep1_s3_workshop.py
Descrição: Dashboard interativo para ajuste de pesos e validação de criticidade.
Objetivo: Apoiar workshops técnicos com especialistas para validar os pesos e critérios usados no modelo de criticidade.

Entradas:
    - Dados: historico_light.csv

Saídas:
    - Dashboard interativo com ajuste de pesos e visualização dos ativos mais críticos.
"""


# Import de bibliotecas

import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

data_path = "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_SUB/script/DADOS/historico_light.csv"

# Carregar os dados


def carregar_dados(caminho):
    """
    Carrega o conjunto de dados de um arquivo CSV.

    Args:
        caminho (str): Caminho para o arquivo CSV.

    Returns:
        pd.DataFrame: DataFrame contendo os dados carregados.
    """
    return pd.read_csv(caminho)

# Função para normalizar variáveis


def normalizar_variavel(df, coluna):
    """
    Normaliza uma coluna específica para o intervalo [0, 1].

    Args:
        df (pd.DataFrame): DataFrame contendo os dados.
        coluna (str): Nome da coluna a ser normalizada.

    Returns:
        pd.Series: Coluna normalizada.
    """
    return (df[coluna] - df[coluna].min()) / (df[coluna].max() - df[coluna].min())


# Inicializar o app Dash
app = dash.Dash(__name__)

# Carregar e preparar os dados
df = carregar_dados(data_path)
df["Frequencia_Falhas_Norm"] = normalizar_variavel(df, "Frequencia_Falhas")
df["Impacto_DEC_FEC_Norm"] = normalizar_variavel(df, "Impacto_DEC_FEC")


def recalcular_criticidade(peso_frequencia, peso_dec):
    """
    Recalcula a criticidade com base nos pesos fornecidos.

    Args:
        peso_frequencia (float): Peso para a frequência de falhas.
        peso_dec (float): Peso para o impacto DEC/FEC.

    Returns:
        pd.DataFrame: DataFrame atualizado com a criticidade recalculada.
    """
    df["Criticidade"] = (
        df["Frequencia_Falhas_Norm"] * peso_frequencia
        + df["Impacto_DEC_FEC_Norm"] * peso_dec
    )
    return df.sort_values(by="Criticidade", ascending=False).head(10)


# Layout do Dashboard
app.layout = html.Div([
    html.H1("Workshop Técnico - Modelo de Criticidade"),
    html.Label("Ajuste os Pesos:"),
    dcc.Slider(0, 1, 0.1, value=0.4, id='peso-frequencia',
               marks={i: f'{i:.1f}' for i in [0, 0.5, 1]}),
    dcc.Slider(0, 1, 0.1, value=0.3, id='peso-dec',
               marks={i: f'{i:.1f}' for i in [0, 0.5, 1]}),
    dcc.Graph(id='grafico-criticidade'),
])

# Callback para atualizar o gráfico


@app.callback(
    Output('grafico-criticidade', 'figure'),
    Input('peso-frequencia', 'value'),
    Input('peso-dec', 'value')
)
def atualizar_grafico(peso_frequencia, peso_dec):
    """
    Atualiza o gráfico com os ativos mais críticos com base nos pesos ajustados.

    Args:
        peso_frequencia (float): Peso para a frequência de falhas.
        peso_dec (float): Peso para o impacto DEC/FEC.

    Returns:
        plotly.graph_objects.Figure: Gráfico de barras atualizado.
    """
    ativos_criticos = recalcular_criticidade(peso_frequencia, peso_dec)
    fig = px.bar(
        ativos_criticos,
        x="ID_Ativo",
        y="Criticidade",
        title="Ativos Mais Críticos (Pesos Ajustados)",
        labels={"ID_Ativo": "ID do Ativo",
                "Criticidade": "Pontuação de Criticidade"},
        template="plotly_white"
    )
    return fig


# Executar o app
if __name__ == '__main__':
    app.run_server(debug=True)
