''' 
    REDE_SUB.docx

    ||> O objetivo é oferecer opções para:

        |> Revisar pesos: Permitir que os pesos das variáveis sejam modificados facilmente no script.
        |> Simular cenários: Gerar rankings com diferentes configurações de pesos.
        |> Validar resultados: Adicionar métricas para verificar robustez do modelo, como correlação entre criticidade e variáveis.
        |> Dashboard Interativo Ajustável: Fornecer um controle no dashboard para ajustar pesos dinamicamente e visualizar os impactos.
            ||> Adaptar o script existente para incorporar essas funcionalidades. Um momento enquanto implemento as alterações.
            ||> O script foi atualizado para atender ao Sprint 3, adicionando funcionalidades de ajuste dinâmico:

        |> Ajuste Dinâmico de Pesos:
            Adicionei sliders no dashboard para modificar os pesos de cada variável diretamente.
            O impacto dos ajustes é refletido nos gráficos em tempo real.
        
        |> Simulações de Cenários:
            Possibilidade de testar diferentes configurações de pesos e observar as mudanças no ranking.
            
        |> Validação Visual:
            Gráficos interativos que mostram como o ranking e as relações variáveis-críticos mudam com os ajustes.

'''

# Import de bibliotecas

import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
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


# Configurações de Caminhos
base_path = "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_SUB/script/DADOS"
input_path = os.path.join(base_path, "ep3_base_normalizada.csv")
output_path = os.path.join(base_path, "matriz_priorizacao_ajustada.csv")

# Pesos iniciais para cálculo da criticidade (ajustáveis no dashboard)
default_weights = {
    "Frequencia_Falhas": 0.4,
    "Tempo_Operacao": 0.3,
    "Numero_Clientes_Afetados": 0.2,
    "Impacto_DEC_FEC": 0.1
}

# Carregar os dados
print("Carregando dados normalizados...")
df = load_normalized_data(input_path)


def create_app(df):
    """
    Cria a aplicação Dash para visualização e ajuste dinâmico de pesos.

    Args:
        df (pd.DataFrame): DataFrame com os dados normalizados.

    Returns:
        Dash: Aplicação Dash configurada.
    """
    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.H1("Validação e Ajustes do Ranking de Criticidade"),
        html.Div([
            html.Label("Frequência de Falhas (Peso):"),
            dcc.Slider(id="peso-falhas", min=0, max=1, step=0.1,
                       value=default_weights["Frequencia_Falhas"]),
            html.Label("Tempo de Operação (Peso):"),
            dcc.Slider(id="peso-operacao", min=0, max=1, step=0.1,
                       value=default_weights["Tempo_Operacao"]),
            html.Label("Número de Clientes Afetados (Peso):"),
            dcc.Slider(id="peso-clientes", min=0, max=1, step=0.1,
                       value=default_weights["Numero_Clientes_Afetados"]),
            html.Label("Impacto DEC/FEC (Peso):"),
            dcc.Slider(id="peso-dec-fec", min=0, max=1, step=0.1,
                       value=default_weights["Impacto_DEC_FEC"]),
        ], style={"margin-bottom": "20px"}),
        dcc.Graph(id="criticidade-bar-chart"),
        dcc.Graph(id="criticidade-scatter")
    ])

    @app.callback(
        [Output("criticidade-bar-chart", "figure"),
         Output("criticidade-scatter", "figure")],
        [Input("peso-falhas", "value"),
         Input("peso-operacao", "value"),
         Input("peso-clientes", "value"),
         Input("peso-dec-fec", "value")]
    )
    def update_charts(w_falhas, w_operacao, w_clientes, w_dec_fec):
        weights = {
            "Frequencia_Falhas": w_falhas,
            "Tempo_Operacao": w_operacao,
            "Numero_Clientes_Afetados": w_clientes,
            "Impacto_DEC_FEC": w_dec_fec
        }

        # Recalcular criticidade
        df_updated = calculate_criticality(df.copy(), weights)

        # Atualizar gráficos
        bar_chart = px.bar(
            df_updated,
            x="Criticidade",
            y="ID_Ativo",
            orientation="h",
            title="Ranking de Criticidade dos Ativos (Ajustado)",
            labels={"ID_Ativo": "Ativo",
                    "Criticidade": "Índice de Criticidade"},
        ).update_layout(yaxis={'categoryorder': 'total ascending'})

        scatter_chart = px.scatter(
            df_updated,
            x="Criticidade",
            y="Frequencia_Falhas",
            size="Numero_Clientes_Afetados",
            color="Impacto_DEC_FEC",
            title="Relação entre Criticidade e Variáveis (Ajustado)",
            labels={"Frequencia_Falhas": "Frequência de Falhas",
                    "Criticidade": "Índice de Criticidade"},
        )

        return bar_chart, scatter_chart

    return app


# Criar e executar a aplicação
app = create_app(df)
print("Executando Dash App com ajuste dinâmico de pesos...")
app.run_server(debug=True)
