from sklearn.preprocessing import LabelEncoder

# Inicializar o LabelEncoder
encoder = LabelEncoder()

def codificar_dados_data_frame(df_train):
    # Aplicar o LabelEncoder nas colunas categóricas do conjunto de treinamento
    df_train_encoded = df_train.apply(lambda x: encoder.fit_transform(x) if x.dtype == 'object' else x)
    return df_train_encoded


def codificar_dados_previsao(data_frame):
    # Codificar o novo caso usando o LabelEncoder ajustado
    df_new_encoded = data_frame.apply(lambda x: encoder.transform(x) if x.dtype == 'object' else x)
    return df_new_encoded
