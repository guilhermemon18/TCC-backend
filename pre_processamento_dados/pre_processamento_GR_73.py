import pandas as pd
from numpy.ma import column_stack
from sklearn.preprocessing import LabelEncoder

from src.pre_processamento_dados.pre_processamento_GR_02 import get_dataframe_gr02_necessary_columns

#Junta os dois datasets gr02 e gr73 de caracterização pelos RAs dos discentes.
#Pré-condição: gr02 dataset não nulo lido do arquivo gr02, gr73 dataset não nulo lido do arquivo gr73
#Pós-condição: Dataframe mesclado com as características de ambos datasets.
def merge_gr73_gr02(gr02, gr73):
    df3 = pd.merge(gr02, gr73, left_on='PssFsc_Codigo', right_on='PssFsc_CdgAcademico')
    return df3

def codificar_variaveis_categoricas_numericas(data_frame):
    # Obtenção dos valores discretos da coluna
    valores_coluna_target = data_frame['TGIStcAtualDescricao'].unique()

    for value in valores_coluna_target:
        if value == 'Formado':
            data_frame.loc[data_frame['TGIStcAtualDescricao'] == value, 'TGIStcAtualDescricao'] = 0
        else:
            data_frame.loc[data_frame['TGIStcAtualDescricao'] == value, 'TGIStcAtualDescricao'] = 1

    # Aplicando Label Encoding para converter valores categóricos (discretos) em números
    # Selecionar apenas as colunas do tipo 'object'
    obj_cols = data_frame.select_dtypes(include=['object']).columns
    # Aplicar o Label Encoding em cada coluna selecionada
    for col in obj_cols:
        le = LabelEncoder()
        data_frame[col] = le.fit_transform(data_frame[col])

    return data_frame

def get_dataframe_gr73():
    print("Olá bom dia!")
    # REalizando a leitura do arquivo excel com os dados:
    base = '../../dadosTCC/'
    nome_arquivo_base_dados = base + 'GR 73_até2018_com ID.xlsx'
    data_frame_gr73 = pd.read_excel(nome_arquivo_base_dados, 'Planilha1')
    data_frame_gr02 = get_dataframe_gr02_necessary_columns()

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
    data_frame = data_frame.sort_values('PrdLtv_Grupo', ascending=True)
    data_frame = data_frame.drop_duplicates(subset='PssFsc_CdgAcademico', keep='first')
    # Remove todas as colunas que a quantidade de dados faltantes é maior que 10% do total de entradas e vazias:
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
    data_frame = data_frame.drop(columns="PrdLtv_Grupo")
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
    data_frame = data_frame.drop(indices_a_remover)

    #agora é possível apagar as linhas que faltam dados:
    data_frame = data_frame.dropna()

    data_frame.to_excel("../../dados_tcc_processados_python/GR 73_até2018_com ID sem cursando.xlsx", index=False)

    #codificando os valores da variável target para evadido(1) não evadido (0)
    #data_frame = codificar_variaveis_categoricas_numericas(data_frame)



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
    data_frame.to_excel("../../dados_tcc_processados_python/GR 73_até2018_com ID processado.xlsx", index=False)
    return data_frame


get_dataframe_gr73()
