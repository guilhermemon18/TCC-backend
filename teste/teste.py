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
