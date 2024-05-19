import pandas as pd

from src.pre_processamento_dados.pre_processamento_GR_30 import get_dataframe_gr30
pd.set_option('display.max_rows', None)  # Exibe todas as linhas
pd.set_option('display.max_columns', None)  # Exibe todas as colunas
dataset = get_dataframe_gr30()

print("Dataset final informações:")
# imprimindo a quantidade de dados no dataset
print('quantidade de dados no data_frame')
data_frame_size = len(dataset.index)
print(data_frame_size)

# Verificar quais colunas têm valores vazios
colunas_com_vazios = dataset.columns[dataset.isna().any()].tolist()
print("Colunas com valores vazios:")
print(colunas_com_vazios)

# Verificar o número de valores ausentes em cada coluna
valores_ausentes = dataset.isnull().sum()
print("Número de valores ausentes em cada atributo:")
print(valores_ausentes)

# Verificar quais colunas estão totalmente vazias
colunas_vazias = dataset.columns[dataset.isna().all()].tolist()

print("Colunas totalmente vazias:")
print(colunas_vazias)

# Verificar o número de valores únicos em cada coluna
num_valores_unicos = dataset.nunique()

# Verificar quais colunas têm apenas um valor único (todos iguais)
colunas_com_mesmo_valor = num_valores_unicos[num_valores_unicos == 1].index.tolist()

print("Atributos com o mesmo valor para todos os registros:")
print(colunas_com_mesmo_valor)
print("Nomes das Colunas no dataset")
print(dataset.columns.tolist())



print("contagem valores: ")
# Loop sobre cada coluna do DataFrame
for column in dataset.columns:
    print(f"Contagem de valores únicos para a coluna '{column}':")
    print(dataset[column].value_counts())
    print()  # Adiciona uma linha em branco entre os resultados de cada coluna

print(dataset.describe())