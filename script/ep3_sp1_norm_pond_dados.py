''' 
    REDE_SUB.docx

    ||> Objetivo: 
    
        |> Revisar e Carregar Dados: Utilizar a base consolidada do Épico 2 (ep2_base_final.csv) como entrada.
        |> Normalização: Aplicar técnicas como Min-Max Scaling para garantir que todas as variáveis estejam entre 0 e 1.
        |> Ponderação: Atribuir pesos específicos às variáveis com base nos critérios definidos no Épico 1.
        |> Documentação: Comentar detalhadamente o código e usar docstrings em todas as funções.
        |> Salvar Saída: Gerar a base ep3_base_normalizada.csv com os dados normalizados e ponderados.
'''

# Import de bibliotecas

import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
import os


def load_data(file_path):
    """
    Carrega os dados a partir de um arquivo CSV.

    Args:
        file_path (str): Caminho para o arquivo CSV.

    Returns:
        DataFrame: Dados carregados como um DataFrame Pandas.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    return pd.read_csv(file_path)


def normalize_columns(df):
    """
    Normaliza colunas numéricas do DataFrame.

    Args:
        df (DataFrame): DataFrame com os dados a serem normalizados.

    Returns:
        DataFrame: DataFrame com colunas normalizadas.
    """
    columns_to_normalize = ["Frequencia_Falhas", "Tempo_Operacao",
                            "Numero_Clientes_Afetados", "Impacto_DEC_FEC"]
    for column in columns_to_normalize:
        if column in df.columns:
            df[column] = (df[column] - df[column].min()) / \
                (df[column].max() - df[column].min())
        else:
            print(f"ATENÇÃO: Coluna '{
                  column}' não encontrada para normalização.")
    return df


def add_year_column(df, date_column):
    """
    Adiciona uma coluna de ano ao DataFrame com base em uma coluna de datas.

    Args:
        df (DataFrame): DataFrame contendo a coluna de datas.
        date_column (str): Nome da coluna de datas.

    Returns:
        DataFrame: DataFrame com a coluna de ano adicionada.
    """
    if date_column not in df.columns:
        raise KeyError(f"A coluna '{date_column}' não existe no DataFrame.")

    df[date_column] = pd.to_datetime(df[date_column], errors="coerce")

    # Verifica valores inválidos na coluna de datas
    invalid_dates = df[df[date_column].isna()]
    if not invalid_dates.empty:
        print(f"ATENÇÃO: Valores de data inválidos encontrados:\n{
              invalid_dates}")
        df = df.dropna(subset=[date_column]).copy()

    df["Ano"] = df[date_column].dt.year
    return df


def save_normalized_data(df, output_path):
    """
    Salva os dados normalizados em um arquivo CSV.

    Args:
        df (DataFrame): DataFrame com os dados normalizados.
        output_path (str): Caminho para salvar o arquivo CSV.
    """
    df.to_csv(output_path, index=False)
    print(f"Base normalizada salva em: {output_path}")


def main():
    """
    Função principal para carregar, normalizar e salvar os dados.
    """
    # Definir caminhos
    base_path = "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_SUB/script/DADOS"
    input_path = os.path.join(base_path, "historico_light.csv")
    output_path = os.path.join(base_path, "ep3_base_normalizada.csv")

    try:
        print("Carregando dados...")
        df = load_data(input_path)

        print("Normalizando colunas...")
        df = normalize_columns(df)

        print("Adicionando coluna de ano...")
        df = add_year_column(df, "Data_Evento")

        print("Salvando dados normalizados...")
        save_normalized_data(df, output_path)
        print("Processo concluído com sucesso!")

    except Exception as e:
        print(f"Erro durante o processamento: {e}")


if __name__ == "__main__":
    main()
