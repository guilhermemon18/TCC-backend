import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from src.pre_processamento_dados.codificacao import codificar_dataframe
from src.pre_processamento_dados.pre_processamento_GR_30 import get_dataframe_gr30
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar e preprocessar os dados
df = get_dataframe_gr30()
df = codificar_dataframe(df)

# Separar features (X) e target (y)
X = df.drop('Situação', axis=1)
y = df['Situação']

# Criar uma instância do classificador de Árvore de Decisão
clf = DecisionTreeClassifier(random_state=42)

# Realizar validação cruzada para avaliação do modelo
cv_scores = cross_val_score(clf, X, y, cv=5)  # cv=5 para 5 folds (divisões) na validação cruzada

# Exibir os scores de validação cruzada
print("Scores de Validação Cruzada:", cv_scores)
print("Média da Acurácia:", np.mean(cv_scores))

# Exibir a matriz de confusão e o relatório de classificação para a última fold
conf_matrix = confusion_matrix(y_test, y_pred)
print('\nMatriz de Confusão:')
print(conf_matrix)

class_report = classification_report(y_test, y_pred, digits=4)
print('\nRelatório de Classificação:')
print(class_report)

# Treinar o modelo usando todos os dados para obter importância dos recursos
clf.fit(X, y)

# Obter a importância dos recursos
importances = clf.feature_importances_

# Criar um DataFrame com as importâncias dos recursos
feature_importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': importances})

# Ordenar os recursos por importância
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

# Plotar a importância dos recursos
plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=feature_importance_df, palette='viridis')
plt.title('Importância dos Recursos - Árvore de Decisão')
plt.xlabel('Importância')
plt.ylabel('Recurso')
plt.show()
