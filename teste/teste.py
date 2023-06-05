import pandas as pd

df = pd.DataFrame({
    'Nome': ['João', 'João', 'Maria', 'Maria', 'Pedro', 'Pedro'],
    'Cargo': ['Analista', 'Coordenador', 'Analista', 'Coordenador', 'Analista', 'Coordenador'],
    'Ano': [2020, 2020, 2020, 2020, 2021, 2021],
    'Salário': [5000, 6000, 4000, 4500, 5500, 6500]
})

print(df)

df_pivot = df.pivot_table(index=['Nome', 'Ano'], columns='Cargo', values='Salário')

print(df_pivot)


# Crie dois DataFrames de exemplo
df1 = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3'],
                    'B': ['B0', 'B1', 'B2', 'B3'],
                    'C': ['C0', 'C1', 'C2', 'C3'],
                    'D': ['D0', 'D1', 'D2', 'D3']})

df2 = pd.DataFrame({'A': ['A0', 'A1', 'A2'],
                    'E': ['B4', 'B5', 'B6'],
                    'F': ['C4', 'C5', 'C6'],
                    'G': ['D4', 'D5', 'D6']})

# Junte os dois DataFrames pela coluna "A"
df3 = pd.merge(df1, df2, on='A')

print(df1)
print(df2)
print(df3)

import pandas as pd

# criando um exemplo de DataFrame com IDs repetidos e informações sobre disciplinas e notas repetidas para cada ID
data = {'id': [1, 1, 2, 2, 3, 3],
        'disciplina': ['matematica', 'portugues', 'matematica', 'portugues', 'matematica', 'portugues'],
        'nota': [8.5, 7.0, 9.0, 8.5, 7.0, 6.5]}

df = pd.DataFrame(data)

# usando o método pivot para transformar as informações de disciplinas e notas em colunas
df_pivot = df.pivot(index='id', columns='disciplina', values='nota')

# renomeando as colunas para ficar mais legível
df_pivot.columns = ['matematica_nota', 'portugues_nota']

# resetando o índice para manter apenas uma linha para cada ID
df_pivot.reset_index(inplace=True)

# visualizando o resultado
print(df_pivot)



import pandas as pd

# Criar um DataFrame de exemplo
data = {
    'ID': [1040, 1040, 1040, 1040],
    'Disciplina': ['A', 'B', 'C', 'C'],
    'Situação': ['Ativa', 'Inativa', 'Inativa', 'Ativa']
}

df = pd.DataFrame(data)

# Ordenar o DataFrame com base na coluna 'Situação' em ordem ascendente
df_sorted = df.sort_values('Situação', ascending=True)

# Remover as duplicatas com base nas colunas 'ID' e 'Disciplina' e manter apenas a primeira ocorrência
df_filtered = df_sorted.drop_duplicates(subset=['ID', 'Disciplina'], keep='first')

# Exibir o DataFrame resultante
print(df_filtered)




