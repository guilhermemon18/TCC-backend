from collections import Counter
import numpy as np
import pandas as pd
import seaborn as sns
from imblearn.over_sampling import SMOTE
from matplotlib import pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from src.pre_processamento_dados.codificacao import codificar_dataframe
from src.pre_processamento_dados.pre_processamento_GR_30 import get_dataframe_gr30

df = get_dataframe_gr30()
df = codificar_dataframe(df)

X = df.drop('Situação', axis=1)
y = df['Situação'].values

print('Original dataset shape %s' % Counter(y))

# SMOTE
smote = SMOTE(random_state=42)
X, y = smote.fit_resample(X, y)

print('Resampled dataset shape %s' % Counter(y))

# 80% dos dados para treino e 20% para teste.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
#np.ravel(Previsor, order="c")



print('Imprimindo informaçoes sobre os dados para analisar o impacto:')
#imprimiindo a quantidade de dados do modelo
print('O dataset de treino possui {} alunos e o de treino {} alunos.'
      .format(X_train.shape[0], X_test.shape[0]))

#LogisticRegression(solver='lbfgs', max_iter=1000), aumenta o número de iteraçoes
clf = LogisticRegression(solver='liblinear', max_iter=10000, random_state=42)


''
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




coefficients = clf.coef_[0]
feature_importance = pd.DataFrame({'Feature': X.columns, 'Importance': np.abs(coefficients)})
feature_importance = feature_importance.sort_values('Importance', ascending=True)
feature_importance.plot(x='Feature', y='Importance', kind='barh', figsize=(10, 6))

print(clf.coef_)
# Obter os coeficientes dos recursos
coefficients = clf.coef_[0]

# Obter os nomes das colunas
data = df.drop("Situação", axis=1)
feature_names = data.columns

# Mostrar a importância de cada recurso
for i, coefficient in enumerate(coefficients):
    print(f"Feature {feature_names[i]}: {abs(coefficient)}")


# Obter os índices dos recursos mais importantes
top_features_indices = coefficients.argsort()[::-1]

# Mostrar os recursos mais importantes
print("Recursos mais importantes:")
for feature_index in top_features_indices:
    print(f"Feature {feature_names[feature_index]}: {abs(coefficients[feature_index])}")

