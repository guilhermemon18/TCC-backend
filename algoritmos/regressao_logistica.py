import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

from src.pre_processamento_dados.pre_processamento_GR_30 import get_dataframe_gr30
from src.pre_processamento_dados.pre_processamento_GR_73 import get_dataframe_gr73

df = get_dataframe_gr30() #get_dataframe_gr73()

# #Estudando como as variáveis impactam na evasão tema do IC:
# print('Correlação das variáveis:')
# print(Base_dados.corr())
# plt.figure(figsize=(10, 7))
# sns.heatmap(Base_dados.corr(),
#             annot = True,
#             fmt = '.2f',
#             cmap='Blues')
# plt.title('Correlação entre variáveis do dataset dos Alunos')
# plt.show()

df = df.drop('PssFsc_CdgAcademico', axis=1)

X = df.drop('AcdStcAtualDescricao', axis=1).values
y = df['AcdStcAtualDescricao'].values

print("Imprimindo os dados usados para treinar: caracteristicas e previsor: ")
print(X)
print(y)


# 80% dos dados para treino e 20% para teste.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
#np.ravel(Previsor, order="c")


print('Imprimindo informaçoes sobre os dados para analisar o impacto:')
#imprimiindo a quantidade de dados do modelo
print('O dataset de treino possui {} alunos e o de treino {} alunos.'
      .format(X_train.shape[0], X_test.shape[0]))

#LogisticRegression(solver='lbfgs', max_iter=1000), aumenta o número de iteraçoes
clf = LogisticRegression(solver='lbfgs', max_iter=10000)



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


# Obter os coeficientes dos recursos
coefficients = clf.coef_[0]

# Obter os nomes das colunas
data = df.drop('AcdStcAtualDescricao', axis=1)
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
