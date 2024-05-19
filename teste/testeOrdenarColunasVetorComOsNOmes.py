import pandas as pd

# Exemplo de DataFrame
data = {
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9],
    'D': [10, 11, 12]
}

df = pd.DataFrame(data)

# Lista de nomes das colunas na ordem desejada
colunasTabelaClassificacao = ['C', 'A', 'D']

# Reordenar as colunas do DataFrame de acordo com a ordem especificada
sub_df = df.reindex(columns=colunasTabelaClassificacao)

print(sub_df)
