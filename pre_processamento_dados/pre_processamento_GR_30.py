import numpy as np
import pandas as pd
from numpy.ma import column_stack
from sklearn.preprocessing import LabelEncoder

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

def merge_gr30_gr73(gr73, gr30):
    df3 = pd.merge(gr73, gr30, left_on='PssFsc_CdgAcademico', right_on='PssFsc_CdgAcademico')
    return df3

def rotular_resultado_disciplinas(data_frame):
    # arrumando as disciplinas por cancelado, reprovado e aprovado no dataSet.
    # if (acdhst_resultado == R && TblGrlItm_DscStcHistorico == Ativa)
    # resultado = reprovado
    # if (acdhst_resultado == R && TblGrlItm_DscStcHistorico == cancelado)
    # resultado = cancelado
    condicoes = [
        (data_frame['AcdHst_Resultado'] == 'R') & (data_frame['TblGrlItm_DscStcHistorico'] == 'Ativa'),
        (data_frame['AcdHst_Resultado'] == 'R') & (data_frame['TblGrlItm_DscStcHistorico'] == 'Cancelada'),
    ]
    valores = ['Reprovado', 'Cancelado']
    data_frame['AcdHst_Resultado'] = np.select(condicoes, valores, default='Aprovado')
    return data_frame

def remover_colunas_desnecessarias(data_frame):
    # removendo colunas de acordo com a olhada no excel:
    data_frame = data_frame.drop(columns="AcdCrs_SqnFormacao")
    data_frame = data_frame.drop(columns="AcdCrs_GrdCrrCodigo")
    data_frame = data_frame.drop(columns="AcdCrs_GrdCrrSrAtual")#não precisa  a série atual
    # porque é sempre primeiro ano que vai investigar, é irrelevante.
    data_frame = data_frame.drop(columns="PrdLetivoIng_Formatacao")
    data_frame = data_frame.drop(columns="AcdStcAtual")
    data_frame = data_frame.drop(columns="AcdHst_SqnHistorico")
    # pode ajudar para verificar se o academico ficou no primeiro ano mais de um ano, mas é para ser igual a PrdLtv_Grupo
    # portanto, pode ser removido!
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
    data_frame = data_frame.drop(columns="TtlAnosCursados")
    return data_frame

def remover_alunos_cursando(data_frame):
    # removendo alunos que estão cursando:
    # Selecione as linhas que atendem à condição e armazene seus índices em uma lista
    # substitua 'coluna' pelo nome da coluna e 'valor' pelo valor a ser buscado
    indices_a_remover = data_frame[data_frame['AcdStcAtualDescricao'] == 'Cursando'].index.tolist()
    # Remova as linhas selecionadas do DataFrame original
    data_frame = data_frame.drop(indices_a_remover)
    return data_frame

def get_dataframe_gr30():
    print("Olá bom dia datasetgr30!")
    # REalizando a leitura do arquivo excel com os dados:
    base = '../../dadosTCC/'
    nome_arquivo_base_dados = base + 'GR 30_2018 _com ID.xlsx'
    data_frame = pd.read_excel(nome_arquivo_base_dados, 'Planilha1')
    # data_frame_gr73 = get_dataframe_gr73()
    # data_frame =
    # Terminando a leitura e guardando-os na variável data_frame.

    info_file_data(data_frame)
    data_frame = basic_processing(data_frame)
    info_file_data(data_frame)
    data_frame = remover_colunas_desnecessarias(data_frame)
    data_frame = remover_alunos_cursando(data_frame)
    # Será utilizado para calcular a idade do academico.:
    # data_frame = data_frame.drop(columns="PrdLetivoIng_Grupo")

    #exemplo de operação entre colunas no pandas: data_frame['AcdHst_Resultado'] = data_frame['coluna1'] + data_frame['coluna2']
    # Remove todas as colunas que a quantidade de dados faltantes é maior que 30% do total de entradas ou vazias:
    data_frame = data_frame.dropna(axis=1, thresh=(get_data_frame_size(data_frame) * 0.7))
    # agora é possível apagar as linhas que faltam dados:
    data_frame = data_frame.dropna()
    data_frame = rotular_resultado_disciplinas(data_frame)
    #Pegar apenas a primeira vez que a pessoa cursou as disciplinas do primeiro ano:
    data_frame = data_frame[(data_frame['PrdLtv_Grupo'] == data_frame['PrdLetivoIng_Grupo']) &
                            (data_frame['AcdHst_GrdCrrSerie'] == 1) & (data_frame['TblGrlItm_DscStcHistorico'] == 'Ativa')]
    #agora que pegou apenas o primeiro ano dá pra excluir a coluna do ano da disciplina:
    data_frame = data_frame.drop(columns="AcdHst_GrdCrrSerie")
    data_frame = data_frame.drop(columns="TblGrlItm_DscStcHistorico")

    #Contando o número de reprovaçoes do aluno:
    #data_frame['QtdDiscplinasReprovado'] = data_frame[data_frame['AcdHst_Resultado'] == 'Reprovado']['PssFsc_CdgAcademico'].value_counts()
    qtdDisciplinasReprovado = data_frame[data_frame['AcdHst_Resultado'] == 'Reprovado']['PssFsc_CdgAcademico'].value_counts()

    #Peguei a primeira vez que a pessoa esteve na universidade também, porque teve pessoas
    #que tiveram várias matriculas no primeiro ano e bateu o mesmo ano que se matriculou com o ano da
    #matricula da disciplina dai ficou duplicado e tive que decidir uma ocorrencia dela no primeiro ano
    #ficou decidida a primeira.
    data_frame = data_frame.sort_values('PrdLetivoIng_Grupo', ascending=True)
    data_frame = data_frame.drop_duplicates(subset=['PssFsc_CdgAcademico', 'Dsc_Descricao'], keep='first')
    data_frame.to_excel("../../dados_tcc_processados_python/GR 30_2018-PIVO.xlsx", index=False)


    # Criando colunas para disciplinas:
    # usando o método pivot para transformar as informações de disciplinas e notas em colunas
    data_frame_pivot = data_frame.pivot(index='PssFsc_CdgAcademico', columns='Dsc_Descricao', values='AcdHst_MdFinal').reset_index()
    # resetando o índice para manter apenas uma linha para cada ID
    data_frame = pd.merge(data_frame, data_frame_pivot, left_on='PssFsc_CdgAcademico', right_on='PssFsc_CdgAcademico')

    data_frame = data_frame.drop_duplicates(subset='PssFsc_CdgAcademico', keep='first')

    

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
