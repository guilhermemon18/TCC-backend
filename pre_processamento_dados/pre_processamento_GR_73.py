import pandas as pd
from numpy.ma import column_stack
from sklearn.impute import KNNImputer
from sklearn.preprocessing import LabelEncoder

from src.pre_processamento_dados.pre_processamento_GR_02 import get_dataframe_gr02_necessary_columns

#Junta os dois datasets gr02 e gr73 de caracterização pelos RAs dos discentes.
#Pré-condição: gr02 dataset não nulo lido do arquivo gr02, gr73 dataset não nulo lido do arquivo gr73
#Pós-condição: Dataframe mesclado com as características de ambos datasets.
def merge_gr73_gr02(gr02, gr73):
    df3 = pd.merge(gr02, gr73, left_on='PssFsc_Codigo', right_on='PssFsc_CdgAcademico')
    return df3


def get_dataframe_gr73(file_gr73 = '../../dadosTCC/GR 73_até2018_com ID.xlsx', file_gr02 = '../../dadosTCC/GR 02_Fabiana Frata_ref_completa.xlsx',
                       is_training_data=True):
    print("Olá bom dia!")
    # REalizando a leitura do arquivo excel com os dados:
    base = '../../dadosTCC/'
    base + 'GR 73_até2018_com ID.xlsx'
    nome_arquivo_base_dados = file_gr73
    data_frame_gr73 = pd.read_excel(nome_arquivo_base_dados, 'Planilha1')
    data_frame_gr02 = get_dataframe_gr02_necessary_columns(file_gr02)

    # imprimindo a quantidade de dados no dataset
    print("Informações GR73:")
    print('quantidade de dados no data_frame')
    data_frame_size = len(data_frame_gr73.index)
    print(data_frame_size)

    # Imprimir a quantidade de atributos no dataset
    print("Quantidade de atributos no dataset:", data_frame_gr73.shape[1])

    # Verificar quais colunas têm valores vazios
    colunas_com_vazios = data_frame_gr73.columns[data_frame_gr73.isna().any()].tolist()
    print("Colunas com valores vazios:")
    print(colunas_com_vazios)

    # Verificar o número de valores ausentes em cada coluna
    valores_ausentes = data_frame_gr73.isnull().sum()
    print("Número de valores ausentes em cada atributo:")
    print(valores_ausentes)

    # Verificar quais colunas estão totalmente vazias
    colunas_vazias = data_frame_gr73.columns[data_frame_gr73.isna().all()].tolist()

    print("Colunas totalmente vazias:")
    print(colunas_vazias)

    # Verificar o número de valores únicos em cada coluna
    num_valores_unicos = data_frame_gr73.nunique()

    # Verificar quais colunas têm apenas um valor único (todos iguais)
    colunas_com_mesmo_valor = num_valores_unicos[num_valores_unicos == 1].index.tolist()

    print("Atributos com o mesmo valor para todos os registros:")
    print(colunas_com_mesmo_valor)
    print("Nomes das Colunas no dataset")
    print(data_frame_gr73.columns.tolist())

    #juntando os dois data-frames com os dados de caracterização necessários
    data_frame = merge_gr73_gr02(data_frame_gr02, data_frame_gr73)
    data_frame.to_excel("../../dados_tcc_processados_python/GR 73_merge_GR02.xlsx", index=False)

    # imprimindo a quantidade de dados no dataset
    print('quantidade de dados no data_frame')
    data_frame_size = len(data_frame.index)
    print(data_frame_size)
    print(data_frame.info())
    print("Tem dados repetidos no dataframe:")
    print(data_frame['PssFsc_CdgAcademico'].duplicated().any())

    # Verificar quais colunas têm valores vazios
    colunas_com_vazios = data_frame.columns[data_frame.isna().any()].tolist()
    print("Colunas com valores vazios:")
    print(colunas_com_vazios)

    # Verificar quais colunas estão totalmente vazias
    colunas_vazias = data_frame.columns[data_frame.isna().all()].tolist()
    print("Colunas totalmente vazias:")
    print(colunas_vazias)


    print("Atributos com o mesmo valor para todos os registros:")
    print(colunas_com_mesmo_valor)
    print("Quantidade colunas com mesmo valor:")
    print(len(colunas_com_mesmo_valor))
    print("Quantidade colunas vazias:")
    print(len(colunas_vazias))
    print("Quantidade de colunas com valores ausentes:")
    print(len(colunas_com_vazios))

    # Imprimindo a quantidade de valores nulos (em branco) e valores totais do dataframe
    print("Quantidade de dados em cada coluna:")
    print(data_frame.count())
    print()
    print("Quantidade de dado NULOS em cada coluna: ")
    print(data_frame.isnull().sum().sort_values(ascending=False)[:10])
    print()


    # Realizando pré_processamento nos dados:
    # Onde não há cor registrada colocar como não declarada:
    data_frame['TblGrlItm_DscCorRaca'] = data_frame['TblGrlItm_DscCorRaca'].fillna('Não declarada')

    # Removendo linhas duplicadas (básico)
    data_frame = data_frame.drop_duplicates()


    # Remove todas as colunas que a quantidade de dados faltantes é maior que 30% do total de entradas e vazias:
    data_frame = data_frame.dropna(axis=1, thresh=(data_frame_size * 0.7))

    # deletando colunas em que todos os dados são iguais
    # Obtendo as colunas com apenas um valor
    colunas_remover = data_frame.columns[data_frame.nunique() == 1]
    # Removendo as colunas com apenas um valor
    data_frame = data_frame.drop(colunas_remover, axis=1)


    #removendo colunas de acordo com a olhada no excel:
    data_frame = data_frame.drop(columns="GrdCrr_Codigo")
    data_frame = data_frame.drop(columns="SrAtual")
    data_frame = data_frame.drop(columns="AcdCrs_SqnFormacao")
    data_frame = data_frame.drop(columns="TblGrlItm_StcAcademico")
    data_frame = data_frame.drop(columns="Ncn_Codigo")
    data_frame = data_frame.drop(columns="PssFsc_DtFalecimento")
    data_frame = data_frame.drop(columns="PrdLtv_Ingresso")
    data_frame = data_frame.drop(columns="PrdLtv_Formatacao")
    data_frame = data_frame.drop(columns="PrcMnc_Codigo")
    data_frame = data_frame.drop(columns="PrcPs_Codigo")
    data_frame = data_frame.drop(columns="End_MlDireta")
    data_frame = data_frame.drop(columns="EndMnc_Codigo")
    data_frame = data_frame.drop(columns="EndUF_Codigo")
    data_frame = data_frame.drop(columns="EndPs_Codigo")
    data_frame = data_frame.drop(columns="TpCrs_codigo")
    data_frame = data_frame.drop(columns="Instituicao")
    data_frame = data_frame.drop(columns="Mnc_Instituicao")
    data_frame = data_frame.drop(columns="TblGrlItm_DscItem1")
    data_frame = data_frame.drop(columns="NatMnc_Codigo")
    data_frame = data_frame.drop(columns="NatMnc_Descricao")
    data_frame = data_frame.drop(columns="NatUF_Codigo")
    data_frame = data_frame.drop(columns="PrdLtv_Situacao")
    data_frame = data_frame.drop(columns="AcdStc_Data")
    data_frame = data_frame.drop(columns="AcdStc_DtExpDiploma")
    data_frame = data_frame.drop(columns="AcdStc_DtClcGrau")
    data_frame = data_frame.drop(columns="AcdStc_DtConclusao")
    data_frame = data_frame.drop(columns="PrcMnc_Descricao")
    data_frame = data_frame.drop(columns="PrcUF_Codigo")
    data_frame = data_frame.drop(columns="PrcPs_Descricao")
    data_frame = data_frame.drop(columns="TpEnd_Descricao")
    #data_frame = data_frame.drop(columns="PrdLtv_Grupo")
    data_frame = data_frame.drop(columns="PssFsc_CdgAcademico")
    data_frame = data_frame.drop(columns="Ncn_Descricao")
    data_frame = data_frame.drop(columns="EndPs_Descricao")

    # removendo alunos que já possuem uma graduação:
    indices_a_remover = data_frame[data_frame['FrmAntTpCrs_Descricao'] == 'Graduação'].index.tolist()
    data_frame = data_frame.drop(indices_a_remover)
    data_frame = data_frame.drop(columns="FrmAntTpCrs_Descricao")

    #removendo alunos que estão cursando:
    # Selecione as linhas que atendem à condição e armazene seus índices em uma lista
    # substitua 'coluna' pelo nome da coluna e 'valor' pelo valor a ser buscado
    indices_a_remover = data_frame[data_frame['TGIStcAtualDescricao'] == 'Cursando'].index.tolist()
    # Remova as linhas selecionadas do DataFrame original
    if is_training_data:
        data_frame = data_frame.drop(indices_a_remover)

    #agora é possível apagar as linhas que faltam dados:
    data_frame = data_frame.dropna()

    data_frame.to_excel("../../dados_tcc_processados_python/GR 73_até2018_com ID processado.xlsx", index=False)
    return data_frame


if __name__ == '__main__':
    get_dataframe_gr73()
