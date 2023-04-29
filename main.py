import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import openpyxl
# If you need to get the column letter, also import this

base = '../'
#dadosFinais2007_6Mat nmome da planilha principal
Base_dados = pd.read_excel(base + 'DADOS_0704.xlsx', 'dadosFinais2007_5Mat')




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


#tema do ic
# tabelas:
print(Base_dados.head())
print(Base_dados.tail())
print(Base_dados.info())
print(Base_dados.describe())

# gráficos de cada coluna do excel
sns.set(font_scale=1.3, rc={'figure.figsize': (20, 20)})
eixo = Base_dados.hist(bins=20, color='blue')
print(eixo)
plt.show()

# blox plot
#plt.figure(figsize=(10, 5))
#sns.boxplot(data=Base_dados, x='Tipo Renda', y='Renda')
#plt.show()

# Separação dos dados de treino e de teste:
Caracteristicas = Base_dados.iloc[:, 1:9].values#obter os valores que definem a resposta, previsão
Previsor = Base_dados.iloc[:, 0:1].values#obter valores de previsão, coluna onde estão os valores resposta.
#Previsor = Previsor.reshape(-1, 1)
#print("Previsões")
#print(Previsor)

#Transformar valores contínuos em discretos!!
#lab = preprocessing.LabelEncoder()
#Caracteristicas = lab.fit_transform(Caracteristicas)
#view transformed values
#print(Caracteristicas)

# 80% dos dados para treino e 20% para teste.
x_treino, x_teste, y_treino, y_teste = train_test_split(Caracteristicas, Previsor.ravel(), test_size=0.30)
#np.ravel(Previsor, order="c")


print('Imprimindo informaçoes sobre os dados para analisar o impacto:')
#imprimiindo a quantidade de dados do modelo
print('O dataset de treino possui {} alunos e o de treino {} alunos.'
      .format(x_treino.shape[0], x_teste.shape[0]))

# gráficos de cada coluna do excel
x_teste = pd.DataFrame(x_teste)
print(Base_dados.IdadeIngresso.describe())
#print(x_teste.IdadeIngresso.describe())

#recomendação de esquecer os dados de teste:
#usar a validação cruzada!
#A validação cruzada nos ajuda a não cometer o erro de usar os dados de teste para avaliar e tentar melhorar o modelo

#LogisticRegression(solver='lbfgs', max_iter=1000), aumenta o número de iteraçoes
Funcao_Logistica = LogisticRegression(solver='lbfgs', max_iter=1000)



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




importance = Funcao_Logistica.coef_[0]
#importance is a list so you can plot it.
feat_importances = pd.Series(importance).nlargest(20).plot(kind='barh',title = 'Feature Importance')
#feat_importances.nlargest(20).plot(kind='barh',title = 'Feature Importance')



#Realizando previsões para um novo cliente

#Salario = 4500
#Tipo_Renda = 1
#Possui_Imovel = 1

#Parametro = [[Salario, Tipo_Renda, Possui_Imovel]]

#Previsao = Funcao_Logistica.predict(Parametro)
#probabilidade de comprar ou n comprar
#Probabilidade = Funcao_Logistica.predict_proba(Parametro)

#if(Previsao == 0):
 #   print('Não vai comprar')
 #   print(Probabilidade)

#else:
 #   print('Vai comprar \o/')
  #  print(Probabilidade)



