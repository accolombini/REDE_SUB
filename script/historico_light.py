'''
    REDE_SUB.docx

        |> Objetivo: este script simples deve gerar uma base para estudos do projeto.
'''

import pandas as pd
import numpy as np
import os

# Definir caminho correto para o diretório de saída
output_dir = "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_SUB/script/DADOS"
output_csv = os.path.join(output_dir, "ep2_base_csv.csv")
output_xlsx = os.path.join(output_dir, "ep2_base_xlsx.xlsx")
output_json = os.path.join(output_dir, "ep2_base_json.json")


def ensure_directory_exists(directory):
    """
    Verifica se o diretório existe e o cria se necessário.

    Args:
        directory (str): Caminho do diretório.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def generate_simulated_data():
    """
    Gera uma base de dados simulada para ativos subterrâneos.

    Returns:
        pd.DataFrame: DataFrame contendo os dados simulados.
    """
    data = {
        "ID_Ativo": [f"A-{str(i).zfill(4)}" for i in range(1, 101)],
        "Frequencia_Falhas": np.random.randint(0, 10, 100),
        "Tempo_Operacao": np.random.uniform(0.5, 50.0, 100),
        "Numero_Clientes_Afetados": np.random.choice([50, 100, 200, 500, 1000], 100),
        "Tipo_Ativo": np.random.choice(["Transformador", "Religador", "Isolador", "Seccionalizador", "Cabo"], 100),
        "Localidade": np.random.choice(["Zona Norte", "Zona Sul", "Centro", "Zona Oeste"], 100),
        "Historico_Manutencao": np.random.choice(["Sim", "Não"], 100),
        "Impacto_DEC_FEC": np.random.uniform(0.0, 50.0, 100),
        "Data_Evento": pd.date_range(start="1990-01-01", periods=100).to_list()
    }
    return pd.DataFrame(data)


# Garante que o diretório de saída existe
ensure_directory_exists(output_dir)

# Gera os dados simulados
df = generate_simulated_data()

# Salva as bases em múltiplos formatos
print("Salvando as bases simuladas...")

# Salvar como CSV
df.to_csv(output_csv, index=False)
print(f"Base CSV salva em: {output_csv}")

# Salvar como Excel
df.to_excel(output_xlsx, index=False)
print(f"Base Excel salva em: {output_xlsx}")

# Salvar como JSON
df.to_json(output_json, orient="records", lines=True)
print(f"Base JSON salva em: {output_json}")
