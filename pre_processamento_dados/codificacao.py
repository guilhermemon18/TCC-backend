import pandas as pd
from src.pre_processamento_dados.pre_processamento_GR_30 import get_dataframe_gr30

codificadoresManual = {
    'Forma de Ingresso': {
        'Vestibular': 0,
        'ENEM': 1,
    },
    'Situação': {
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
    'Tipo Instituição De Origem': {
        'Privada': 0,
        'Pública': 1
    },
    'Cotista': {
        'N': 0,
        'S': 1
    }
}

colunas_codificar_cor = ['Cor_Amarela',	'Cor_Branca', 'Cor_Não declarada', 'Cor_Parda', 'Cor_Preta']

# Invertendo chaves e valores para criar um dicionário de decodificadores
decodificadoresManual = {
    coluna: {
        valor: chave for chave, valor in codificadores.items()
    }
    for coluna, codificadores in codificadoresManual.items()
}


def codificar_dataframe(dataframe):
    # Codificar as colunas usando o dicionário
    dataframe_codificado = dataframe.replace(codificadoresManual)
    # Codificar a coluna "Cor" usando o OneHotEncode
    dataframe_cores = pd.get_dummies(dataframe_codificado['Cor'], prefix='Cor', dtype=int)
    dataframe_codificado = dataframe_codificado.drop(columns=['Cor'])
    # dataframe_codificado = pd.concat([dataframe_codificado, dataframe_cores])
    dataframe_codificado = dataframe_codificado.join(dataframe_cores)
    for coluna in colunas_codificar_cor:
        if coluna not in dataframe_codificado.columns:
            # A coluna não existe, então vamos criá-la e definir todos os valores como 'valor_padrao'
            dataframe_codificado[coluna] = 0
    return dataframe_codificado


def decodificar_dataframe(dataframe_codificado):
    dataframe_decodificado = dataframe_codificado.replace(decodificadoresManual)
    # Pegar todas as colunas que começam com "Cor"
    colunas_cor = [coluna for coluna in dataframe_decodificado.columns if coluna.startswith('Cor_')]
    # Reverter as colunas codificadas em uma única coluna
    dataframe_decodificado['Cor'] = dataframe_decodificado[colunas_cor].idxmax(axis=1).str.replace('Cor_', '')
    # Excluir as colunas codificadas
    dataframe_decodificado = dataframe_decodificado.drop(columns=colunas_cor)
    return dataframe_decodificado


def codificar_instancia(instancia, codificadores):
    instancia_codificada = instancia.copy()

    for coluna, codificador in codificadores.items():
        instancia_codificada[coluna] = codificador.transform([instancia[coluna]])[0]

    return instancia_codificada



if __name__ == '__main__':
    data_frame = get_dataframe_gr30()
    data_frame_codificado = codificar_dataframe(data_frame)
    data_frame_codificado.to_excel("../../dados_tcc_processados_python/GR 30 CODIFICADO.xlsx",
                        index=False)
    data_frame_decoficado = decodificar_dataframe(data_frame_codificado)
    data_frame_decoficado.to_excel("../../dados_tcc_processados_python/GR 30 DECODIFICADO.xlsx",
                        index=False)
