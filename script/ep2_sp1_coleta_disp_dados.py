''' 
    REDE_SUB

        ||> Objetivo:
            Coletar dados: Ele verifica e carrega os dados disponíveis em diferentes formatos fornecidos pela Light (CSV, Excel e JSON).
            Consolidar dados: Une as diferentes bases de dados em um único DataFrame, removendo duplicatas.
            Salvar os dados consolidados: Gera uma base única no formato CSV, pronta para análise ou uso em etapas posteriores.
            
            |> Considerações do simulador:
                Certifique-se de que os arquivos ep2_base_csv.csv, ep2_base_xlsx.xlsx e ep2_base_json.json estejam no diretório especificado em data_directory.
                Execute o script para gerar o arquivo consolidado ep2_dados_consolidados.csv no mesmo diretório.   

        ||> O que esperamos desse script:
            
            |> Carga de Dados:
                Os dados de três fontes diferentes (ep2_base_csv.csv, ep2_base_xlsx.xlsx, ep2_base_json.json) foram carregados corretamente.
                Tratamento para leitura de JSON, garantindo compatibilidade com diferentes orientações de dados.

            |> Consolidação:
                Todos os dados foram concatenados em um único DataFrame.
                Duplicatas foram removidas, o que evita redundâncias.
                
            |> Saída:
                Os dados consolidados foram salvos em ep2_dados_consolidados.csv.
'''

# Import bibliotecas

import pandas as pd
import os


def ensure_directory_exists(directory):
    """
    Verifica se o diretório existe e o cria se necessário.

    Args:
        directory (str): Caminho do diretório.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def load_and_consolidate_data(data_directory):
    """
    Carrega dados de múltiplos formatos (CSV, Excel, JSON) e consolida em um único DataFrame.

    Args:
        data_directory (str): Caminho do diretório contendo os arquivos de dados.

    Returns:
        pd.DataFrame: DataFrame consolidado contendo todos os dados.
    """
    # Definir caminhos dos arquivos
    csv_path = os.path.join(data_directory, "ep2_base_csv.csv")
    xlsx_path = os.path.join(data_directory, "ep2_base_xlsx.xlsx")
    json_path = os.path.join(data_directory, "ep2_base_json.json")

    # Verificar se os arquivos existem
    for file_path in [csv_path, xlsx_path, json_path]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    # Carregar dados
    print("Carregando dados...")
    df_csv = pd.read_csv(csv_path)
    df_xlsx = pd.read_excel(xlsx_path)

    # Ler JSON linha por linha (orientação de múltiplas linhas)
    try:
        df_json = pd.read_json(json_path, lines=True)
    except ValueError:
        df_json = pd.read_json(json_path, orient="records")

    # Consolidar os dados
    print("Consolidando dados...")
    consolidated_df = pd.concat([df_csv, df_xlsx, df_json], ignore_index=True)

    # Remover duplicatas
    consolidated_df.drop_duplicates(inplace=True)

    return consolidated_df


def main():
    """
    Função principal para carregar, consolidar e salvar os dados em formato padronizado.
    """
    # Caminho do diretório de dados
    data_directory = "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_SUB/script/DADOS"
    output_path = os.path.join(data_directory, "ep2_dados_consolidados.csv")

    # Garantir que o diretório de saída existe
    ensure_directory_exists(data_directory)

    # Consolidar dados
    consolidated_df = load_and_consolidate_data(data_directory)

    # Salvar dados consolidados
    consolidated_df.to_csv(output_path, index=False)
    print(f"Dados consolidados salvos em: {output_path}")


if __name__ == "__main__":
    main()
