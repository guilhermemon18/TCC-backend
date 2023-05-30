from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
import pandas as pd
from src.pre_processamento_dados import pre_processamento_GR_30
from src.pre_processamento_dados.pre_processamento_GR_30 import get_dataframe_gr30

# Carregue um conjunto de dados de exemplo
df = get_dataframe_gr30()
print(type(df))
X = df.drop('AcdStcAtualDescricao', axis=1).values
y = df['AcdStcAtualDescricao'].values

# Divida os dados em conjunto de treinamento e conjunto de teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

# Crie uma instância do classificador de árvore de decisão
clf = DecisionTreeClassifier()

# Treine o modelo usando o conjunto de treinamento
clf.fit(X_train, y_train)

# Faça previsões no conjunto de teste
y_pred = clf.predict(X_test)

# Avalie a precisão do modelo
print("Precisão:", metrics.accuracy_score(y_test, y_pred))
