'''
    ATIVOS_REDE_SUB.docx
    Objetivo: este script simples tem por objetivo apenas testar e valiidar se o ambiente virtual está configurado adequadamente para o projeto.
'''

# Importando as bibliotecas necessárias
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from ydata_profiling import ProfileReport

# Geração de um dataset sintético para validação
print("Gerando dataset sintético...")
X, y = make_classification(
    n_samples=1000,
    n_features=10,
    n_informative=5,
    n_redundant=2,
    random_state=42
)

# Criando um DataFrame para testes
df = pd.DataFrame(X, columns=[f"Feature_{i}" for i in range(1, 11)])
df["Target"] = y

# Criando um perfilamento do dataset com ydata-profiling
print("Gerando relatório de perfilamento...")
profile = ProfileReport(df, title="Relatório de Perfilamento do Dataset")
profile.to_file("perfilamento_dataset.html")

# Divisão do dataset em treino e teste
print("Dividindo o dataset em treino e teste...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)

# Treinamento de um modelo simples
print("Treinando modelo Random Forest...")
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Avaliação do modelo
print("Avaliando o modelo...")
y_pred = model.predict(X_test)
print("\nRelatório de Classificação:\n", classification_report(y_test, y_pred))
print("\nMatriz de Confusão:\n", confusion_matrix(y_test, y_pred))

# Criando visualizações com Matplotlib, Seaborn e Plotly
print("Criando visualizações...")

# Gráfico de dispersão com Seaborn
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="Feature_1", y="Feature_2",
                hue="Target", palette="viridis")
plt.title("Dispersão das Features 1 e 2 (Seaborn)")
plt.savefig("scatter_seaborn.png")
plt.show()

# Gráfico interativo com Plotly
fig = px.scatter(
    df, x="Feature_1", y="Feature_2", color="Target",
    title="Dispersão das Features 1 e 2 (Plotly)"
)
fig.write_html("scatter_plotly.html")
fig.show()

# Finalização
print("Script executado com sucesso! Verifique os arquivos gerados.")
