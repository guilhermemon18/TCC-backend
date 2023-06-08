import numpy as np
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from src.pre_processamento_dados.pre_processamento_GR_30 import get_dataframe_gr30

# Carregue um conjunto de dados de exemplo
df = get_dataframe_gr30()
df = df.drop('PssFsc_CdgAcademico', axis=1)

X = df.drop('AcdStcAtualDescricao', axis=1).values
y = df['AcdStcAtualDescricao'].values

# Divida os dados em conjunto de treinamento e conjunto de teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Criar o classificador Random Forest
clf = RandomForestClassifier()

# Treine o modelo usando o conjunto de treinamento
clf.fit(X_train, y_train)

# Faça previsões no conjunto de teste
y_pred = clf.predict(X_test)

# Avalie a precisão do modelo
print("Acurácia:", metrics.accuracy_score(y_test, y_pred))

# confusion_matriz: matriz de confusão
print('Matriz de confusão:')
print(confusion_matrix(y_test, y_pred))
#mostra a precisão do modelo
print(classification_report(y_test, y_pred,  digits=4))


# Obter a importância dos recursos
importances = clf.feature_importances_

# Obter os nomes das colunas
data = df.drop('AcdStcAtualDescricao', axis=1)
feature_names = data.columns

# Mostrar a importância de cada recurso
for i, importance in enumerate(importances):
    print(f"Feature {feature_names[i]}: {importance}")

# Obter os índices dos recursos mais importantes
top_features_indices = np.argsort(importances)[::-1]

# Mostrar os recursos mais importantes
print("Recursos mais importantes:")
for feature_index in top_features_indices:
    print(f"Feature {feature_names[feature_index]}: {importances[feature_index]}")
