from collections import Counter

import numpy as np
from imblearn.over_sampling import SMOTE
from pandas import DataFrame
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

from src.pre_processamento_dados.codificacao import codificar_dataframe, decodificar_dataframe
from src.pre_processamento_dados.pre_processamento_GR_30 import get_dataframe_gr30

df = get_dataframe_gr30()
df = codificar_dataframe(df)
#LogisticRegression(solver='lbfgs', max_iter=1000), aumenta o número de iteraçoes
clf = LogisticRegression(solver='liblinear', max_iter=10000, random_state=42)
# df = df.drop('PssFsc_CdgAcademico', axis=1)

X = df.drop('Situação', axis=1)
print("Features treinamento: ")
print(df.columns)
y = df['Situação'].values

print("Imprimindo os dados usados para treinar: caracteristicas e previsor: ")
print(X)
print(y)

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


def predict(data_frame: DataFrame):
    data_frame_codificado = codificar_dataframe(data_frame)
    data_frame_codificado_sem_nome = data_frame_codificado.drop(columns=['Nome', 'Situação', 'Registro Acadêmico (RA)'])
    print("Features x usando algoritmo: ")
    print(data_frame_codificado_sem_nome.columns)
    previsoes = clf.predict(data_frame_codificado_sem_nome.values)
    probabilidades = clf.predict_proba(data_frame_codificado_sem_nome.values)
    print(previsoes)
    print(probabilidades)
    # Probabilidades associadas à classe prevista para cada instância
    probabilidades_classe_prevista = np.choose(previsoes, probabilidades.T) * 100
    probabilidades_classe_prevista = np.round(probabilidades_classe_prevista, 2)  # Arredonda para duas casas decimais
    # Imprimir previsões e probabilidades associadas à classe prevista
    for previsao, probabilidade_classe in zip(previsoes, probabilidades_classe_prevista):
        print(f'Previsão: {previsao}, Probabilidade para a classe prevista: {probabilidade_classe}')

    data_frame_predito = data_frame_codificado.copy()
    data_frame_predito = data_frame_predito.drop(columns=['Situação'])
    data_frame_predito['Situação'] = previsoes
    data_frame_predito['Probabilidade(%)'] = probabilidades_classe_prevista
    data_frame_predito = decodificar_dataframe(data_frame_predito)
    print(data_frame_predito)
    return data_frame_predito





