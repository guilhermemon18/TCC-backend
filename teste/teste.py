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

