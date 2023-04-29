import numpy as np
import pandas as pd
from numpy.ma import column_stack
from sklearn.preprocessing import LabelEncoder

from src.pre_processamento_dados.pre_processamento_GR_02 import get_dataframe_gr02_necessary_columns


def get_data_frame_size(data_frame):
    return len(data_frame.index)

def info_file_data(data_frame):
    # imprimindo a quantidade de dados no dataset
    print('quantidade de dados no data_frame')
    data_frame_size = get_data_frame_size(data_frame)
    print(data_frame_size)

    # Imprimindo a quantidade de valores nulos (em branco) e valores totais do dataframe
    print("Quantidade de dados em cada coluna:")
    print(data_frame.count())
    print()
    print("Quantidade de dado NULOS em cada coluna: ")
    print(data_frame.isnull().sum().sort_values(ascending=False)[:20])
    print()

def basic_processing(data_frame):
    # Removendo linhas duplicadas (básico)
    data_frame = data_frame.drop_duplicates()
    # deletando colunas em que todos os dados são iguais
    # Obtendo as colunas com apenas um valor
    colunas_remover = data_frame.columns[data_frame.nunique() == 1]
    # Removendo as colunas com apenas um valor
    return data_frame.drop(colunas_remover, axis=1)
def get_dataframe_gr30():
    # REalizando a leitura do arquivo excel com os dados:
    base = '../../dadosTCC/'
    nome_arquivo_base_dados = base + 'GR 30_2018 _com ID.xlsx'
    data_frame = pd.read_excel(nome_arquivo_base_dados, 'Planilha1')
    # Terminando a leitura e guardando-os na variável data_frame.

    info_file_data(data_frame)
    data_frame = basic_processing(data_frame)
    info_file_data(data_frame)

    #removendo colunas de acordo com a olhada no excel:
    data_frame = data_frame.drop(columns="AcdCrs_SqnFormacao")
    data_frame = data_frame.drop(columns="AcdCrs_GrdCrrCodigo")
    data_frame = data_frame.drop(columns="PrdLetivoIng_Formatacao")
    data_frame = data_frame.drop(columns="AcdStcAtual")
    data_frame = data_frame.drop(columns="AcdHst_SqnHistorico")
    #pode ajudar para verificar se o academico ficou no primeiro ano mais de um ano, mas é para ser igual a PrdLtv_Grupo
    #portanto, pode ser removido!
    data_frame = data_frame.drop(columns="PrdLtv_Formatacao")
    data_frame = data_frame.drop(columns="AcdHst_MdPrdLetivo")
    data_frame = data_frame.drop(columns="AcdHst_NtExame")
    data_frame = data_frame.drop(columns="TblGrlItm_CdgStcDscHistorico")
    data_frame = data_frame.drop(columns="Dsc_ChTotal")
    data_frame = data_frame.drop(columns="AcdHst_GrdCrrCodigo")
    data_frame = data_frame.drop(columns="PrdLtv_PrdLetivo")
    data_frame = data_frame.drop(columns="TtlFaltas")
    data_frame = data_frame.drop(columns="TblGrlItm_FrmOferta")
    data_frame = data_frame.drop(columns="AcdHst_TpMatricula")
    data_frame = data_frame.drop(columns="PrdLtv_GrpInicial")
    data_frame = data_frame.drop(columns="TrfPrdLtvOrgCursados")
    data_frame = data_frame.drop(columns="AnosContados")

    #Será utilizado para calcular a idade do academico.:
    #data_frame = data_frame.drop(columns="PrdLetivoIng_Grupo")
    #data_frame = data_frame.drop(columns="TblGrlItm_DscStcHistorico")

    #data_frame = data_frame.loc[data_frame['AcdHst_Resultado'] == 'A']

    #exemplo de operação entre colunas no pandas: data_frame['AcdHst_Resultado'] = data_frame['coluna1'] + data_frame['coluna2']

    #arrumando as disciplinas por cancelado, reprovado e aprovado no dataSet.
    condicoes = [
        (data_frame['AcdHst_Resultado'] == 'R') & (data_frame['TblGrlItm_DscStcHistorico'] == 'Ativa'),
        (data_frame['AcdHst_Resultado'] == 'R') & (data_frame['TblGrlItm_DscStcHistorico'] == 'Cancelada'),
    ]
    valores = ['Reprovado', 'Cancelado']
    data_frame['AcdHst_Resultado'] = np.select(condicoes, valores, default='Aprovado')

    #data_frame = data_frame.pivot(index='PssFsc_CdgAcademico', columns='Dsc_Descricao', values='AcdHst_MdFinal')

    # Remove todas as colunas que a quantidade de dados faltantes é maior que 30% do total de entradas ou vazias:
    data_frame = data_frame.dropna(axis=1, thresh=(get_data_frame_size(data_frame) * 0.7))

    #agora é possível apagar as linhas que faltam dados:
    data_frame = data_frame.dropna()

    #if (acdhst_resultado == R && TblGrlItm_DscStcHistorico == Ativa)
        #resultado = reprovado
    #if (acdhst_resultado == R && TblGrlItm_DscStcHistorico == cancelado)
        #resultado = cancelado



    #removendo alunos que estão cursando:
    # Selecione as linhas que atendem à condição e armazene seus índices em uma lista
    # substitua 'coluna' pelo nome da coluna e 'valor' pelo valor a ser buscado
    indices_a_remover = data_frame[data_frame['AcdStcAtualDescricao'] == 'Cursando'].index.tolist()
    # Remova as linhas selecionadas do DataFrame original
    data_frame = data_frame.drop(indices_a_remover)
    print(data_frame['AcdStcAtualDescricao'].tail)
    data_frame.to_excel("../../dados_tcc_processados_python/GR 30_2018_com ID sem cursando.xlsx", index=False)


    #codificando os valores da variável target para evadido(1) não evadido (0)
    # Obtenção dos valores discretos da coluna
    valores_coluna_target = data_frame['AcdStcAtualDescricao'].unique()

    for value in valores_coluna_target:
        if value == 'Formado':
            data_frame.loc[data_frame['AcdStcAtualDescricao'] == value, 'AcdStcAtualDescricao'] = 0
        else:
            data_frame.loc[data_frame['AcdStcAtualDescricao'] == value, 'AcdStcAtualDescricao'] = 1


    print(data_frame['AcdStcAtualDescricao'])
    #Aplicando Label Encoding para converter valores categóricos (discretos) em números
    # Selecionar apenas as colunas do tipo 'object'
    obj_cols = data_frame.select_dtypes(include=['object']).columns
    # Aplicar o Label Encoding em cada coluna selecionada
    for col in obj_cols:
        le = LabelEncoder()
        data_frame[col] = le.fit_transform(data_frame[col])



    # imprimindo a quantidade de dados no dataset
    print('quantidade de dados no data_frame')
    data_frame_size = len(data_frame.index)
    print(data_frame_size)

    # Imprimindo a quantidade de valores nulos (em branco) e valores totais do dataframe
    print("Quantidade de dados em cada coluna:")
    print(data_frame.count())
    print()
    print("Quantidade de dado NULOS em cada coluna: ")
    print(data_frame.isnull().sum().sort_values(ascending=False)[:10])
    print()

    # tabelas:
    print(data_frame.info())
    print(data_frame.describe())
    print(data_frame['AcdStcAtualDescricao'])
    data_frame.to_excel("../../dados_tcc_processados_python/GR 30_2018 _com ID processado.xlsx",index=False)
    return data_frame


get_dataframe_gr30()
