''' 
    REDE_SUB

    Objetivo: limpeza e o tratamento inicial de dados referem-se a etapas fundamentais para preparar os dados brutos antes de realizar análises mais avançadas ou criar modelos. No contexto deste sprint, os principais passos de limpeza e tratamento inicial implementados (ou planejados) são:

    1. Remoção de Valores Duplicados
        Por quê?: Dados duplicados podem distorcer análises, introduzir redundâncias e prejudicar a integridade dos resultados.
        Ação: Identificar e remover linhas duplicadas no DataFrame.
    2. Identificação e Correção de Inconsistências
        Por quê?: Inconsistências, como erros de digitação, formatos diferentes para o mesmo valor, ou unidades não padronizadas, dificultam análises.
        Ação:
        Padronizar formatos (datas, strings, números).
        Uniformizar unidades de medida, se aplicável.
    3. Preenchimento de Lacunas (Valores Nulos ou Faltantes)
        Por quê?: Dados faltantes podem causar erros ou limitações em análises e modelos.
        Ação:
        Preenchimento de valores nulos com:
        Média ou mediana (para dados numéricos).
        Modas ou categorias padrão (para dados categóricos).
        Regressão ou interpolação (em casos mais sofisticados).
    4. Conversão e Unificação de Formatos
        Por quê?: Formatos despadronizados (ex.: diferentes tipos de data ou números com vírgulas e pontos) podem gerar erros.
        Ação:
        Garantir que todos os dados numéricos estejam no mesmo formato.
        Converter colunas de datas para um formato datetime unificado.
    5. Documentação das Ações
        Por quê?: A transparência e a rastreabilidade são essenciais para validar o trabalho feito.
        Ação:
        Registro das alterações realizadas em um log ou diretamente como comentários no código.
    6. Exportação dos Dados Tratados
        Por quê?: Manter uma versão limpa e tratada para análises futuras.
        Ação:
        Exportar o DataFrame tratado para um novo arquivo consolidado e documentado.

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


def clean_and_treat_data(input_path, output_path):
    """
    Realiza limpeza e tratamento inicial dos dados.

    Args:
        input_path (str): Caminho do arquivo de dados consolidado.
        output_path (str): Caminho para salvar a base tratada.

    Returns:
        pd.DataFrame: DataFrame tratado e limpo.
    """
    # Carregar os dados
    print("Carregando dados...")
    df = pd.read_csv(input_path)

    # Remover duplicatas
    print("Removendo duplicatas...")
    df.drop_duplicates(inplace=True)

    # Corrigir formatos (exemplo: converter colunas numéricas para float)
    print("Corrigindo formatos...")
    numeric_columns = ["Frequencia_Falhas", "Impacto_DEC_FEC"]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Preencher valores faltantes com a média
    print("Preenchendo valores faltantes...")
    for col in numeric_columns:
        df[col].fillna(df[col].mean(), inplace=True)

    # Documentar as alterações
    print("Documentando alterações...")
    with open(os.path.join(os.path.dirname(output_path), "documentacao_tratamento.txt"), "w") as doc_file:
        doc_file.write("Tratamento Realizado:\n")
        doc_file.write("- Remoção de duplicatas\n")
        doc_file.write("- Correção de formatos nas colunas numéricas\n")
        doc_file.write("- Preenchimento de valores faltantes com a média\n")

    # Salvar dados tratados
    print("Salvando dados tratados...")
    df.to_csv(output_path, index=False)
    print(f"Base tratada salva em: {output_path}")

    return df


def main():
    """
    Função principal para executar o script de limpeza e tratamento dos dados.
    """
    # Caminhos de entrada e saída
    input_path = "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_SUB/script/DADOS/ep2_dados_consolidados.csv"
    output_path = "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_SUB/script/DADOS/ep2_dados_tratados.csv"

    # Garantir que o diretório de saída existe
    ensure_directory_exists(os.path.dirname(output_path))

    # Limpeza e tratamento dos dados
    clean_and_treat_data(input_path, output_path)


if __name__ == "__main__":
    main()
