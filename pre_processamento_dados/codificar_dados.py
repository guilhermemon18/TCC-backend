# from sklearn.preprocessing import LabelEncoder
#
# # Inicializar o LabelEncoder
# encoder = LabelEncoder()
# colunas_codificar = []
#
# def codificar_dados_data_frame(df):
#     # Codifique as colunas selecionadas
#     global colunas_codificar
#     colunas_codificar = df.select_dtypes(include=['object']).columns
#     for coluna in colunas_codificar:
#         df[coluna] = encoder.fit_transform(df[coluna])
#     # # Aplicar o LabelEncoder nas colunas categóricas do conjunto de treinamento
#     # df_train_encoded = df_train.apply(lambda x: encoder.fit_transform(x) if x.dtype == 'object' else x)
#     # return df_train_encoded
#
# def codificar_dados_previsao(data_frame):
#     # Codificar o novo caso usando o LabelEncoder ajustado
#     df_new_encoded = data_frame.apply(lambda x: encoder.transform(x) if x.dtype == 'object' else x)
#     return df_new_encoded
#
#
# def decodificar_dados_data_frame(data_frame):
#     # Decodificar o DataFrame
#     data_frame = data_frame.apply(lambda x: encoder.inverse_transform(x) if x.dtype == 'int64' else x)
#     return data_frame
#
import json

import joblib
import numpy as np
from sklearn.preprocessing import LabelEncoder


def codificar_dados(dataset, colunas=None):
    if colunas == None:
        colunas = dataset.select_dtypes(include=['object']).columns
    print(colunas)
    codificadores = {}
    dataset_codificado = dataset.copy()

    for coluna in colunas:
        codificador = LabelEncoder()
        dataset_codificado[coluna] = codificador.fit_transform(dataset[coluna])
        codificadores[coluna] = codificador

    return dataset_codificado, codificadores


def decodificar_dados(dataset_codificado, codificadores= None):
    if codificadores == None:
        codificadores= carregar_codificadores('../../files/codificadores.json')
    dataset_decodificado = dataset_codificado.copy()
    print(codificadores)
    for coluna, codificador in codificadores.items():
        dataset_decodificado[coluna] = codificador.inverse_transform(dataset_codificado[coluna])

    return dataset_decodificado


def salvar_codificadores(codificadores, arquivo= None):
    codificadores_salvos = {}
    if arquivo == None:
        arquivo = '../../files/codificadores.json'
    for coluna, codificador in codificadores.items():
        codificadores_salvos[coluna] = {
            'classes': codificador.classes_.tolist(),
            'codigos': codificador.transform(codificador.classes_).tolist()
        }

    with open(arquivo, 'w') as f:
        json.dump(codificadores_salvos, f)


def carregar_codificadores(arquivo):
    with open(arquivo, 'r') as f:
        codificadores_salvos = json.load(f)

    codificadores = {}
    print(codificadores_salvos)
    for coluna, info in codificadores_salvos.items():
        print(info['classes'])
        print(info['codigos'])
        codificador = LabelEncoder()
        codificador.classes_ = np.array(info['classes'])
        codificador.transform = np.vectorize(lambda x: info['codigos'][info['classes'].index(x)])
        codificadores[coluna] = codificador


    return codificadores


def codificar_dataframe(dataframe, codificadores):
    dataframe_codificado = dataframe.copy()

    for coluna, codificador in codificadores.items():
        dataframe_codificado[coluna] = codificador.transform(dataframe[coluna])

    return dataframe_codificado


def codificar_instancia(instancia, codificadores):
    instancia_codificada = instancia.copy()

    for coluna, codificador in codificadores.items():
        instancia_codificada[coluna] = codificador.transform([instancia[coluna]])[0]

    return instancia_codificada



def carregar_codificadores(arquivo):
    with open(arquivo, 'r') as f:
        codificadores_salvos = json.load(f)

    codificadores = {}
    for coluna, info in codificadores_salvos.items():
        codificador = LabelEncoder()
        codificador.classes_ = np.array(info['classes'])
        codificadores[coluna] = codificador

    return codificadores


def codificar_dataframe(dataframe, codificadores):
    dataframe_codificado = dataframe.copy()

    for coluna, codificador in codificadores.items():
        dataframe_codificado[coluna] = codificador.transform(dataframe[coluna])

    return dataframe_codificado


def decodificar_dataframe(dataframe_codificado, codificadores):
    dataframe_decodificado = dataframe_codificado.copy()

    for coluna, codificador in codificadores.items():
        dataframe_decodificado[coluna] = codificador.inverse_transform(dataframe_codificado[coluna])

    return dataframe_decodificado


def salvar_codificadores(codificadores, arquivo=None):
    codificadores_salvos = {}
    if arquivo is None:
        arquivo = '../../files/codificadores.json'
    for coluna, codificador in codificadores.items():
        codificadores_salvos[coluna] = {
            'classes': codificador.classes_.tolist(),
            'codigos': codificador.transform(codificador.classes_).tolist()
        }

    with open(arquivo, 'w') as f:
        json.dump(codificadores_salvos, f)
