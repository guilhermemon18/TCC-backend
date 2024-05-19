import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# Novos dados de previsão com apenas 'branco' e 'preto'
novos_dados = pd.DataFrame({'cor': ['branco', 'preto']})

# Definir todas as categorias possíveis
categorias_possiveis = ['pardo', 'preto', 'branco', 'amarelo', 'não especificado']

# Criar um codificador one-hot com as categorias definidas
encoder = OneHotEncoder(categories=[categorias_possiveis], sparse=False)

# Ajustar e transformar os dados de previsão
novos_dados_encoded = encoder.fit_transform(novos_dados[['cor']])

# Converter em DataFrame pandas
novos_dados_encoded_df = pd.DataFrame(novos_dados_encoded, columns=encoder.get_feature_names_out(['cor']))

# Agora novos_dados_encoded_df está pronto para fazer previsões
