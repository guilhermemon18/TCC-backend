import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

from src.pre_processamento_dados.pre_processamento_GR_30 import get_dataframe_gr30
from src.pre_processamento_dados.pre_processamento_GR_73 import get_dataframe_gr73

Base_dados = get_dataframe_gr30() #get_dataframe_gr73()

print(Base_dados)
print()
print()
#Estudando como as variáveis impactam na evasão tema do IC:
print('Correlação das variáveis:')
print(Base_dados.corr())
plt.figure(figsize=(10, 7))
sns.heatmap(Base_dados.corr(),
            annot = True,
            fmt = '.2f',
            cmap='Blues')
plt.title('Correlação entre variáveis do dataset dos Alunos')
plt.show()

# Separação dos dados de treino e de teste:
Caracteristicas = Base_dados.iloc[:, 1:9].values#obter os valores que definem a resposta, previsão
Previsor = Base_dados.iloc[:, 0:1].values#obter valores de previsão, coluna onde estão os valores resposta.

Base_dados = Base_dados.drop('PssFsc_CdgAcademico', axis=1)

Caracteristicas = Base_dados.drop('AcdStcAtualDescricao', axis=1).values
Previsor = Base_dados['AcdStcAtualDescricao'].values

print("Imprimindo os dados usados para treinar: caracteristicas e previsor: ")
print(Caracteristicas)
print(Previsor)


# 80% dos dados para treino e 20% para teste.
x_treino, x_teste, y_treino, y_teste = train_test_split(Caracteristicas, Previsor, test_size=0.20)
#np.ravel(Previsor, order="c")


print('Imprimindo informaçoes sobre os dados para analisar o impacto:')
#imprimiindo a quantidade de dados do modelo
print('O dataset de treino possui {} alunos e o de treino {} alunos.'
      .format(x_treino.shape[0], x_teste.shape[0]))

#LogisticRegression(solver='lbfgs', max_iter=1000), aumenta o número de iteraçoes
Funcao_Logistica = LogisticRegression(solver='lbfgs', max_iter=10000)



# vai fitar os dados, aplicando as fórmulas da regressao logistica
Funcao_Logistica.fit(x_treino, y_treino)
# função para fazer as previões.
print('Comparando resultados do y_teste com o predict!')
Previsoes = Funcao_Logistica.predict(x_teste)
print('Predict:')
print(Previsoes)
print("teste")
print(y_teste)
# confusion_matriz: matriz de confusão
print('Matriz de confusão:')
print(confusion_matrix(y_teste, Previsoes))
#mostra a precisão do modelo
print(classification_report(y_teste, Previsoes,  digits=4))
# Mostrando importância de cada feature
#verificando os dados que são impactantes para a evasão:
