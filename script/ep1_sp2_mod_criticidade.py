'''
    REDE_SUB

    |> Objetivo:
        ||> Estrutura Preliminar de Pontuação
                Criar um modelo de pontuação inicial com base nas variáveis identificadas na Sprint 1:
                Frequência de Falhas: Quanto maior, maior o peso na criticidade.
                Tempo de Operação: Ativos mais antigos tendem a ser mais críticos.
                Impacto DEC/FEC: Correlação direta com a criticidade.
                Número de Clientes Afetados: Quanto maior o impacto, maior o peso.
            |> Normalizar as variáveis para garantir que todas contribuam de forma proporcional.

        ||> Definir Pesos Iniciais
                Atribuir pesos baseados na análise de impacto realizada:
                Exemplo inicial:
                Frequência de Falhas: 40%
                Tempo de Operação: 20%
                Impacto DEC/FEC: 30%
                Número de Clientes Afetados: 10%
            |> Permitir ajustes futuros nos pesos conforme feedback.

        ||> Simulação de Cenários
                Avaliar a robustez do modelo gerando diferentes cenários com combinações variadas de variáveis.
                Identificar ativos mais críticos para priorização.

            |> Dois cenários alternativos foram definidos:
                Cenário 1: Maior peso para Frequencia_Falhas (50%) e menor peso para Tempo_Operacao (10%).
                Cenário 2: Pesos equilibrados para Frequencia_Falhas, Tempo_Operacao, e Impacto_DEC_FEC (30% cada).
'''

import pandas as pd
import numpy as np
import plotly.express as px

# Caminho para os dados
data_path = "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_SUB/script/DADOS/historico_light.csv"
df = pd.read_csv(data_path)

# **Docstring**
"""
Modelo inicial de criticidade:
1. Calcula uma pontuação preliminar para cada ativo.
2. Usa pesos atribuídos às variáveis relevantes.
3. Simula cenários e identifica ativos mais críticos.
4. Compara resultados entre cenários para validação da robustez.
5. Exporta os resultados finais.
"""

# **Normalização das Variáveis**


def normalize(column):
    """
    Normaliza uma coluna para o intervalo [0, 1].
    """
    return (column - column.min()) / (column.max() - column.min())


# Aplicando a normalização às variáveis selecionadas
df["Frequencia_Falhas_Norm"] = normalize(df["Frequencia_Falhas"])
df["Tempo_Operacao_Norm"] = normalize(df["Tempo_Operacao"])
df["Impacto_DEC_FEC_Norm"] = normalize(df["Impacto_DEC_FEC"])
df["Numero_Clientes_Afetados_Norm"] = normalize(df["Numero_Clientes_Afetados"])

# **Pesos Iniciais**
pesos = {
    "Frequencia_Falhas_Norm": 0.4,
    "Tempo_Operacao_Norm": 0.2,
    "Impacto_DEC_FEC_Norm": 0.3,
    "Numero_Clientes_Afetados_Norm": 0.1
}

# **Cálculo da Pontuação de Criticidade**


def calcular_criticidade(row, pesos):
    """
    Calcula a pontuação de criticidade com base nos pesos atribuídos.
    """
    return sum(row[var] * peso for var, peso in pesos.items())


df["Criticidade"] = df.apply(calcular_criticidade, axis=1, pesos=pesos)

# **Simulação de Cenários**
"""
Simula diferentes configurações de pesos para avaliar a robustez do modelo de criticidade.
"""
cenarios = {
    "Cenário 1": {"Frequencia_Falhas_Norm": 0.5, "Tempo_Operacao_Norm": 0.1, "Impacto_DEC_FEC_Norm": 0.3, "Numero_Clientes_Afetados_Norm": 0.1},
    "Cenário 2": {"Frequencia_Falhas_Norm": 0.3, "Tempo_Operacao_Norm": 0.3, "Impacto_DEC_FEC_Norm": 0.3, "Numero_Clientes_Afetados_Norm": 0.1}
}

# Gerar criticidade para cada cenário
for cenario, pesos_alt in cenarios.items():
    df[f"Criticidade_{cenario}"] = df.apply(
        calcular_criticidade, axis=1, pesos=pesos_alt)

# **Identificar Ativos Mais Críticos por Cenário**
for cenario in cenarios.keys():
    print(f"\nAtivos mais críticos no {cenario}:")
    ativos_criticos_cenario = df.sort_values(
        by=f"Criticidade_{cenario}", ascending=False).head(10)
    print(ativos_criticos_cenario[["ID_Ativo", f"Criticidade_{cenario}"]])

    # Visualizar ativos mais críticos para o cenário atual
    fig = px.bar(
        ativos_criticos_cenario,
        x="ID_Ativo",
        y=f"Criticidade_{cenario}",
        title=f"Ativos Mais Críticos - {cenario}",
        labels={"ID_Ativo": "ID do Ativo", f"Criticidade_{
            cenario}": "Pontuação de Criticidade"},
        template="plotly_white"
    )
    fig.show()

# **Comparar Criticidade Entre Cenários**
"""
Compara as pontuações de criticidade entre os cenários para os ativos mais críticos do modelo inicial.
"""
ativos_top = df.sort_values(by="Criticidade", ascending=False).head(10)
comparacao_cenarios = ativos_top[["ID_Ativo", "Criticidade"] +
                                 [f"Criticidade_{cenario}" for cenario in cenarios.keys()]]

fig = px.line(
    comparacao_cenarios.melt(
        id_vars="ID_Ativo",
        var_name="Cenário",
        value_name="Valor_Criticidade"  # Nome ajustado para evitar conflito
    ),
    x="ID_Ativo",
    y="Valor_Criticidade",
    color="Cenário",
    title="Comparação de Criticidade Entre Cenários",
    labels={"ID_Ativo": "ID do Ativo",
            "Valor_Criticidade": "Pontuação de Criticidade"},
    template="plotly_white"
)
fig.show()

# **Exportar Resultados**
"""
Exporta os resultados finais para um arquivo CSV.
"""
output_path = "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_SUB/script/DADOS/criticidade_resultados.csv"
df.to_csv(output_path, index=False)
print(f"Resultados exportados para: {output_path}")
