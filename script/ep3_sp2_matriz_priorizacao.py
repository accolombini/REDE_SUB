''' 
    REDE_SUB.docx

    ||> Objetivo: 
        
        |> Carregar os Dados: Os dados normalizados são carregados para um DataFrame.
        |> Calcular a Matriz de Priorização: A matriz é ordenada pela ponderação total, e uma nova coluna é adicionada para representar a prioridade.
        |> Salvar os Dados: A matriz de priorização é salva em um arquivo CSV.
        |> Criar Visualizações Interativas: Um dashboard interativo é gerado usando Dash e Plotly para explorar a matriz de priorização.
        |> As linhas representariam os ativos ou IDs.
        |> As colunas seriam as variáveis ponderadas ou categorias.
        |> Uma coluna adicional indicaria a prioridade (geralmente como índice ou na última coluna).

        ||> Conceito e Aplicação
            A análise multicritério busca consolidar múltiplos fatores de decisão em uma única métrica, ponderando a relevância de cada variável no contexto analisado. No caso, utilizamos as variáveis:
            Frequência de Falhas (Frequencia_Falhas): Indica o número de interrupções associadas ao ativo.
            Tempo de Operação (Tempo_Operacao): Mede há quanto tempo o ativo está em uso, o que pode indicar desgaste.
            Número de Clientes Afetados (Numero_Clientes_Afetados): Representa o impacto direto em usuários.
            Impacto DEC/FEC (Impacto_DEC_FEC): Relaciona-se à influência regulatória do ativo.
            Cada variável foi normalizada para valores entre 0 e 1, garantindo comparabilidade. Em seguida, atribuíram-se pesos para cada variável, refletindo sua importância relativa:
                Frequência de Falhas: Peso 0.4
                Tempo de Operação: Peso 0.3
                Número de Clientes Afetados: Peso 0.2
                Impacto DEC/FEC: Peso 0.1
        
        ||> Interpretação Gráfica
            
            Os gráficos ajudam a interpretar os resultados:
            Ranking de Criticidade (Bar Chart):
            Ordena os ativos pelo índice de criticidade.
            Útil para priorizar manutenções.
            Relação entre Criticidade e Variáveis (Scatter Plot):
            Permite identificar padrões e correlações entre criticidade e fatores como frequência de falhas, número de clientes afetados, etc.
            Bolhas maiores indicam maior impacto em clientes, enquanto a cor reflete o impacto regulatório.
            Diferenciais
            Normalização: Garante que variáveis com escalas diferentes sejam comparáveis.
            Ponderação: Ajusta a importância relativa de cada variável, alinhando com objetivos estratégicos.
            Visualizações Dinâmicas: Facilita a comunicação e interpretação dos resultados para diferentes públicos, como especialistas e gestores.

'''

# Import de bibliotecas

import pandas as pd
import dash
from dash import dcc, html
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
output_path = os.path.join(base_path, "matriz_priorizacao.csv")

# Pesos para cálculo da criticidade (ajustar conforme necessário)
weights = {
    "Frequencia_Falhas": 0.4,
    "Tempo_Operacao": 0.3,
    "Numero_Clientes_Afetados": 0.2,
    "Impacto_DEC_FEC": 0.1
}

# Carregar e processar os dados
try:
    print("Carregando dados normalizados...")
    df = load_normalized_data(input_path)

    print("Calculando criticidade...")
    df = calculate_criticality(df, weights)

    print("Salvando matriz de priorização...")
    save_criticality_matrix(df, output_path)

    # Dash para visualização
    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.H1("Matriz de Priorização de Ativos Subterrâneos"),
        dcc.Graph(
            id="criticidade-bar-chart",
            figure=px.bar(
                df,
                x="Criticidade",
                y="ID_Ativo",
                orientation="h",
                title="Ranking de Criticidade dos Ativos",
                labels={"ID_Ativo": "Ativo",
                        "Criticidade": "Índice de Criticidade"},
            ).update_layout(yaxis={'categoryorder': 'total ascending'})
        ),
        dcc.Graph(
            id="criticidade-scatter",
            figure=px.scatter(
                df,
                x="Criticidade",
                y="Frequencia_Falhas",
                size="Numero_Clientes_Afetados",
                color="Impacto_DEC_FEC",
                title="Relação entre Criticidade e Variáveis",
                labels={"Frequencia_Falhas": "Frequência de Falhas",
                        "Criticidade": "Índice de Criticidade"},
            )
        )
    ])

    print("Executando Dash App...")
    app.run_server(debug=True)

except Exception as e:
    print(f"Erro durante o processamento: {e}")
