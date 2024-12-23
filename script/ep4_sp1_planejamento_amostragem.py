''' 
    REDE_SUB.py

        ||> Objetivo: planejamento da amostragem estatística.

        ||> Revisar os Dados Consolidados:
            Usar a matriz de priorização gerada no Épico 3 para identificar os ativos mais críticos.
            Ordenar e agrupar os ativos com base nos índices de criticidade.
            
        ||> Aplicar Amostragem Estatística:
            Selecionar uma amostra representativa com base em métodos como:
                Amostragem Estratificada: Separar ativos por faixas de criticidade ou regiões.
                Amostragem Aleatória Simples: Selecionar ativos de forma aleatória entre os mais críticos.
        
        ||>Gerar um Plano Detalhado:
            Salvar a lista de ativos selecionados para inspeção em um arquivo CSV.
            Gerar visualizações (gráficos) que facilitem o entendimento do plano de amostragem.

        ||> Incorporação de Feedback:
            Adicionada uma função para carregar ajustes de criticidade vindos de um arquivo CSV (feedback_campo.csv).
            Os valores de criticidade são atualizados com base no feedback, caso sejam fornecidos.
            Flexibilidade:
            O script continua funcionando mesmo se o arquivo de feedback não existir, garantindo robustez.
            Permite ajustes iterativos conforme o feedback evolui.
            Fluxo Atualizado:
            Após carregar a matriz original, o feedback é incorporado antes de gerar a amostragem estratificada.
'''

# Import bibliotecas

import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import norm
import os


def load_criticality_matrix(file_path):
    """
    Carrega a matriz de criticidade a partir de um arquivo CSV.

    Args:
        file_path (str): Caminho para o arquivo CSV da matriz de criticidade.

    Returns:
        pd.DataFrame: DataFrame com os dados da matriz de criticidade.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    return pd.read_csv(file_path)


def stratified_sampling(df, strata_column, sample_size):
    """
    Realiza amostragem estratificada com base em uma coluna de estratos.

    Args:
        df (pd.DataFrame): DataFrame com os dados de entrada.
        strata_column (str): Nome da coluna usada para estratificação.
        sample_size (int): Tamanho total da amostra desejada.

    Returns:
        pd.DataFrame: DataFrame com a amostra estratificada.
    """
    strata = df[strata_column].value_counts(normalize=True)
    strata_sample_sizes = (strata * sample_size).round().astype(int)

    sampled_df = pd.DataFrame()
    for strata_value, n_samples in strata_sample_sizes.items():
        sampled_strata = df[df[strata_column] == strata_value].sample(
            n=min(n_samples, len(df[df[strata_column] == strata_value])), random_state=42)
        sampled_df = pd.concat([sampled_df, sampled_strata])

    return sampled_df


def update_sampling_based_on_feedback(df, feedback_path):
    """
    Atualiza os dados com base no feedback da equipe de campo.

    Args:
        df (pd.DataFrame): DataFrame original com os dados da matriz de criticidade.
        feedback_path (str): Caminho para o arquivo CSV contendo o feedback.

    Returns:
        pd.DataFrame: DataFrame atualizado com o feedback incorporado.
    """
    if not os.path.exists(feedback_path):
        print("Arquivo de feedback não encontrado. Continuando sem ajustes.")
        return df

    feedback = pd.read_csv(feedback_path)
    df = df.merge(feedback, on="ID_Ativo", how="left")

    # Aplicar ajustes baseados no feedback (exemplo: ajustar criticidade)
    if 'Ajuste_Criticidade' in feedback.columns:
        df['Criticidade'] = df['Ajuste_Criticidade'].combine_first(
            df['Criticidade'])

    return df


def create_feedback_template(output_path):
    """
    Gera um arquivo de template para o feedback da equipe de campo.

    Args:
        output_path (str): Caminho para salvar o template de feedback.
    """
    template_data = {
        "ID_Ativo": ["A001", "A002", "A003"],
        "Ajuste_Criticidade": [0.75, 0.60, 0.85],
        "Observacoes": ["Criticidade ajustada após inspeção.", "Ativo em boas condições.", "Necessita de reparos urgentes."]
    }
    feedback_df = pd.DataFrame(template_data)
    feedback_df.to_csv(output_path, index=False)
    print(f"Template de feedback gerado em: {output_path}")


def save_sampling_plan(df, output_path):
    """
    Salva o plano de amostragem em um arquivo CSV.

    Args:
        df (pd.DataFrame): DataFrame contendo o plano de amostragem.
        output_path (str): Caminho para salvar o arquivo CSV.
    """
    df.to_csv(output_path, index=False)
    print(f"Plano de amostragem salvo em: {output_path}")


def main():
    """
    Executa o script principal para gerar o plano de amostragem.
    """
    # Configurações de Caminhos
    base_path = "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_SUB/script/DADOS"
    input_path = os.path.join(base_path, "matriz_priorizacao.csv")
    feedback_path = os.path.join(base_path, "feedback_campo.csv")
    output_path = os.path.join(base_path, "plano_amostragem.csv")

    # Gerar template de feedback, se necessário
    if not os.path.exists(feedback_path):
        print("Gerando template de feedback...")
        create_feedback_template(feedback_path)

    # Carregar a matriz de criticidade
    print("Carregando a matriz de criticidade...")
    df = load_criticality_matrix(input_path)

    # Incorporar feedback da equipe de campo
    print("Incorporando feedback da equipe de campo...")
    df = update_sampling_based_on_feedback(df, feedback_path)

    # Definir critérios para estratos (Exemplo: Criticidade em 3 níveis)
    print("Definindo estratos com base na criticidade...")
    df['Estrato'] = pd.qcut(df['Criticidade'], q=3, labels=[
                            'Baixa', 'Média', 'Alta'])

    # Aplicar amostragem estratificada
    print("Executando amostragem estratificada...")
    sample_size = 50  # Ajustar conforme necessidade
    sampled_df = stratified_sampling(df, 'Estrato', sample_size)

    # Salvar o plano de amostragem
    print("Salvando o plano de amostragem...")
    save_sampling_plan(sampled_df, output_path)

    # Visualização do plano
    print("Gerando visualização da amostragem...")
    fig = px.histogram(sampled_df, x='Estrato', color='Estrato',
                       title="Distribuição de Amostra por Estrato")
    fig.show()


if __name__ == "__main__":
    main()
