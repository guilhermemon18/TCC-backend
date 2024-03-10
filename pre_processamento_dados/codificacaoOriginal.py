from sklearn.preprocessing import LabelEncoder
import joblib

# Criando um dicionário de associação de nomes
colunas = {
    'Acd_TpIngresso': 'FormaIngresso',
    'QtdDiscplinasReprovado': 'NúmeroDisciplinasReprovado1ºano',
    'PssFsc_Sexo': 'Sexo',
    'EndMnc_Descricao': 'Endereço',
    'FrmAntInsCtgAdministrativa': 'TipoInstituiçãoDeOrigem',
    'OcpVgaCotista': 'Cotista',
    'TblGrlItm_DscCorRaca': 'Cor'
}

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


def codificar_dados(dataframe):
    codificadores = {}
    dataframe_codificado = dataframe.copy()

    for coluna in dataframe.select_dtypes(include=['object']).columns:
        codificador = LabelEncoder()
        dataframe_codificado[coluna] = codificador.fit_transform(dataframe[coluna])
        codificadores[coluna] = codificador

    return dataframe_codificado, codificadores


def decodificar_dados(dataframe_codificado, codificadores):
    dataframe_decodificado = dataframe_codificado.copy()

    for coluna, codificador in codificadores.items():
        dataframe_decodificado[coluna] = codificador.inverse_transform(dataframe_codificado[coluna])

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
