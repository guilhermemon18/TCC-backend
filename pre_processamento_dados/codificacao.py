from sklearn.preprocessing import LabelEncoder
import joblib

codificadoresManual = {
    'FormaIngresso': {
        'Vestibular': 0,
        'Enem': 1,
    },
    'AcdStcAtualDescricao': {
        'Formado': 0,
        'Evadido': 1
    },
    'Sexo': {
        'F': 0,
        'M': 1
    },
    'Endereço': {
        'Dentro da Região de Foz': 0,
        'Fora da Região de Foz': 1
    },
    'TipoInstituiçãoDeOrigem': {
        'Privada': 0,
        'Pública': 1
    },
    'Cotista': {
        'N': 0,
        'S': 1
    }
}

# Invertendo chaves e valores para criar um dicionário de decodificadores
decodificadoresManual = {
    coluna: {
        valor: chave for chave, valor in codificadores.items()
    }
    for coluna, codificadores in codificadoresManual.items()
}


def codificar_dados(dataframe):
    # Codificar as colunas usando o dicionário
    dataframe_codificado = dataframe.replace(codificadoresManual)
    return dataframe_codificado


def decodificar_dados(dataframe_codificado):
    dataframe_decodificado = dataframe_codificado.replace(decodificadoresManual)
    return dataframe_decodificado


def codificar_instancia(instancia, codificadores):
    instancia_codificada = instancia.copy()

    for coluna, codificador in codificadores.items():
        instancia_codificada[coluna] = codificador.transform([instancia[coluna]])[0]

    return instancia_codificada


def codificar_dataframe(dataframe, codificadores):
    dataframe_codificado = dataframe.copy()

    for coluna, codificador in codificadores.items():
        dataframe_codificado[coluna] = codificador.transform(dataframe[coluna])

    return dataframe_codificado


def salvar_codificadores(codificadores, arquivo):
    joblib.dump(codificadores, arquivo)


def carregar_codificadores(arquivo):
    return joblib.load(arquivo)
