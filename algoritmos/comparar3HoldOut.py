from collections import Counter

import numpy as np
from imblearn.over_sampling import SMOTE, ADASYN
from imblearn.under_sampling import NearMiss, OneSidedSelection, RandomUnderSampler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from src.pre_processamento_dados.codificacao import codificar_dataframe
from src.pre_processamento_dados.pre_processamento_GR_30 import get_dataframe_gr30
import graphviz

df = get_dataframe_gr30()
df = codificar_dataframe(df)

X = df.drop('Situação', axis=1).values
y = df['Situação'].values


print('Original dataset shape %s' % Counter(y))

# SMOTE
smote = SMOTE(random_state=42)
X, y = smote.fit_resample(X, y)

print('Resampled dataset shape %s' % Counter(y))

# Divida os dados em conjunto de treinamento e conjunto de teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Crie uma instância do classificador de árvore de decisão
clf = DecisionTreeClassifier(random_state=42)

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




# Criar o classificador Random Forest
clf = RandomForestClassifier(random_state=42)

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




#LogisticRegression(solver='lbfgs', max_iter=1000), aumenta o número de iteraçoes
clf = LogisticRegression(solver='liblinear', max_iter=10000, random_state=42)



# vai fitar os dados, aplicando as fórmulas da regressao logistica
clf.fit(X_train, y_train)
# função para fazer as previões.
print('Comparando resultados do y_teste com o predict!')
y_pred = clf.predict(X_test)
print('Predict:')
print(y_pred)
print("teste")
print(y_test)
# confusion_matriz: matriz de confusão
print('Matriz de confusão:')
print(confusion_matrix(y_test, y_pred))
#mostra a precisão do modelo
print(classification_report(y_test, y_pred, digits=4))
# Mostrando importância de cada feature
#verificando os dados que são impactantes para a evasão: