import pandas as pd

# Seu DataFrame de exemplo
data = {'Cor': ['Vermelho', 'Azul', 'Verde', 'Vermelho']}
df = pd.DataFrame(data)

# Codificar a coluna "Cor" usando o OneHotEncode
df_encoded = pd.get_dummies(df['Cor'], prefix='Cor', dtype=int)

# Exibir o DataFrame resultante
print(df_encoded)

# Decodificar os valores codificados
df_decoded = pd.DataFrame({'Cor': df_encoded.idxmax(axis=1)})

# Exibir o DataFrame resultante
print(df_decoded)

import pandas as pd

# DataFrame de exemplo com as colunas codificadas e outras colunas
data = {
    'Outra_Coluna': [1, 2, 3],
    'Cor_Azul': [0, 1, 0],
    'Cor_Verde': [1, 0, 0],
    'Cor_Vermelho': [0, 0, 1]
}
df_encoded = pd.DataFrame(data)

# Pegar todas as colunas que começam com "Cor"
colunas_cor = [coluna for coluna in df_encoded.columns if coluna.startswith('Cor_')]

# Reverter as colunas codificadas em uma única coluna
df_encoded['Cor'] = df_encoded[colunas_cor].idxmax(axis=1).str.replace('Cor_', '')

# Excluir as colunas codificadas
df_encoded.drop(columns=colunas_cor, inplace=True)

# Exibir o DataFrame resultante
print(df_encoded)



import pandas as pd

# Função para codificar o DataFrame
def codificar_dataframe(dataframe, colunas_a_codificar):
    # Copiar o DataFrame original para evitar modificações indesejadas
    df_codificado = dataframe.copy()

    # Codificar apenas as colunas especificadas usando get_dummies
    for coluna in colunas_a_codificar:
        df_codificado = pd.concat([df_codificado.drop(columns=[coluna]), pd.get_dummies(df_codificado[coluna], prefix=coluna)], axis=1)

    return df_codificado

# Função para decodificar o DataFrame
def decodificar_dataframe(dataframe, colunas_a_decodificar):
    # Copiar o DataFrame codificado para evitar modificações indesejadas
    df_decodificado = dataframe.copy()

    # Decodificar as colunas especificadas
    for coluna in colunas_a_decodificar:
        prefixo = coluna.split('_')[0]  # Obtém o prefixo da coluna (o nome original da coluna)
        df_decodificado[prefixo] = df_decodificado.filter(like=prefixo).idxmax(axis=1).str.split('_', expand=True)[1]

    # Remover as colunas codificadas
    df_decodificado = df_decodificado.drop(columns=colunas_a_decodificar)

    return df_decodificado

# Exemplo de uso
data = {
    'Outra_Coluna1': [1, 2, 3],
    'Outra_Coluna2': [4, 5, 6],
    'Cor': ['Vermelho', 'Azul', 'Verde'],
    'Tamanho': ['Pequeno', 'Médio', 'Grande']
}
df = pd.DataFrame(data)

# Colunas a serem codificadas
colunas_a_codificar = ['Cor']

# Colunas a serem decodificadas (se necessário)
colunas_a_decodificar = ['Cor_Vermelho', 'Cor_Azul', 'Cor_Verde']

# Codificar o DataFrame
df_codificado = codificar_dataframe(df, colunas_a_codificar)
print("DataFrame Codificado:")
print(df_codificado)

# Decodificar o DataFrame (opcional)
df_decodificado = decodificar_dataframe(df_codificado, colunas_a_decodificar)
print("\nDataFrame Decodificado:")
print(df_decodificado)


