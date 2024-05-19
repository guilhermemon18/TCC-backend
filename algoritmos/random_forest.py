from collections import Counter

import pandas as pd
import seaborn as sns
import numpy as np
from imblearn.over_sampling import SMOTE
from matplotlib import pyplot as plt
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_auc_score, roc_curve

from src.pre_processamento_dados.codificacao import codificar_dataframe
from src.pre_processamento_dados.pre_processamento_GR_30 import get_dataframe_gr30


df = get_dataframe_gr30()
df = codificar_dataframe(df)
X = df.drop('Situação', axis=1)
y = df['Situação'].values


print('Original dataset shape %s' % Counter(y))

# # NearMiss
# nm = NearMiss()
# X, y = nm.fit_resample(X, y)

# # OneSidedSelection (Algoritmo tipo KNN)
# oss = OneSidedSelection(random_state=42)
# X, y = oss.fit_resample(X, y)
#
# # Random Undersampler
# rus = RandomUnderSampler(random_state=42)
# X, y = rus.fit_resample(X, y)

# SMOTE
smote = SMOTE(random_state=42)
X, y = smote.fit_resample(X, y)

print('Resampled dataset shape %s' % Counter(y))


# Divida os dados em conjunto de treinamento e conjunto de teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)



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

# Calcular a curva ROC
fpr, tpr, thresholds = roc_curve(y_test, y_pred)

# Calcular a área sob a curva ROC (AUC)
auc = roc_auc_score(y_test, y_pred)

# Plotar a curva ROC
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {auc:.2f})')
plt.plot([0, 1], [0, 1], linestyle='--', color='red', label='Classificador Aleatório')
plt.plot([0, 0, 1], [0, 1, 1], color='green', lw=2, linestyle=':', label='Classificador Perfeito')
plt.xlabel('Taxa de Falso Positivo')
plt.ylabel('Taxa de Verdadeiro Positivo')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend()
plt.show()


# Obter a importância dos recursos
importances = clf.feature_importances_

# Criar um DataFrame com as importâncias dos recursos
feature_importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': importances})

# Ordenar os recursos por importância
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
# Selecionar apenas os 10 principais recursos
feature_importance_df = feature_importance_df.head(10)
# Plotar a importância dos recursos
plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=feature_importance_df, palette='viridis')
plt.title('Importância de Atributos - Floresta Aleatória', fontsize=12)
plt.xlabel('Importância', fontsize=12)
plt.ylabel('Atributo', fontsize=12)
plt.show()

# Calcular a matriz de confusão
cm = confusion_matrix(y_test, y_pred)

# Plotar a matriz de confusão
plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, xticklabels=["Formado", "Evadido"],
            yticklabels=["Formado", "Evadido"], annot_kws={"size": 12})
plt.xlabel('Classe prevista')
plt.ylabel('Classe esperada')
plt.title('Matriz de Confusão')
plt.show()








# # Obter a importância dos recursos
# importances = clf.feature_importances_
#
# # Obter os nomes das colunas
# data = df.drop('Situação', axis=1)
# feature_names = data.columns
#
# # Mostrar a importância de cada recurso
# for i, importance in enumerate(importances):
#     print(f"Feature {feature_names[i]}: {importance}")
#
# # Obter os índices dos recursos mais importantes
# top_features_indices = np.argsort(importances)[::-1]
#
# # Mostrar os recursos mais importantes
# print("Recursos mais importantes:")
# for feature_index in top_features_indices:
#     print(f"Feature {feature_names[feature_index]}: {importances[feature_index]}")
#
# # Extrair a importância dos atributos
# importances = clf.feature_importances_
#
# # Criar um DataFrame com os nomes dos atributos e suas importâncias
# feature_importances = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
#
# # Ordenar os atributos por importância
# feature_importances = feature_importances.sort_values(by='Importance', ascending=False)
#
# # Plotar a importância dos atributos
# plt.figure(figsize=(10, 6))
# sns.barplot(x='Importance', y='Feature', data=feature_importances, palette='viridis')
# plt.title('Importância dos Atributos - Floresta Aleatória')
# plt.xlabel('Importância')
# plt.ylabel('Atributo')
# plt.show()
