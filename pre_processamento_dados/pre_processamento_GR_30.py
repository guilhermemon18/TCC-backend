import numpy as np
import pandas as pd
from numpy.ma import column_stack
from pandas import DataFrame
from sklearn.preprocessing import LabelEncoder

from src.pre_processamento_dados.codificar_dados import codificar_dados, salvar_codificadores, carregar_codificadores, \
    decodificar_dados, codificar_dataframe, codificar_instancia
from src.pre_processamento_dados.pre_processamento_GR_73 import get_dataframe_gr73


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
    elemento = 'PrdLetivoIng_Grupo'
    # if elemento in colunas_remover:
    #     colunas_remover.remove(elemento)
    colunas_remover = colunas_remover.drop(elemento, errors='ignore')
    #Removendo as colunas com apenas um valor
    return data_frame.drop(colunas_remover, axis=1)


def merge_gr30_gr73(gr30, gr73):
    df3 = pd.merge(gr30, gr73, left_on='PssFsc_CdgAcademico', right_on='PssFsc_Codigo', suffixes=('_left', '_right'))
    df3 = df3.drop(columns='PssFsc_Codigo')
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
    data_frame = data_frame.drop(columns="AcdCrs_SqnFormacao", errors='ignore')
    data_frame = data_frame.drop(columns="AcdCrs_GrdCrrCodigo", errors='ignore')
    data_frame = data_frame.drop(columns="AcdCrs_GrdCrrSrAtual", errors='ignore')  # não precisa  a série atual
    # porque é sempre primeiro ano que vai investigar, é irrelevante.
    data_frame = data_frame.drop(columns="PrdLetivoIng_Formatacao", errors='ignore')
    data_frame = data_frame.drop(columns="AcdStcAtual", errors='ignore')
    data_frame = data_frame.drop(columns="AcdHst_SqnHistorico", errors='ignore')
    # pode ajudar para verificar se o academico ficou no primeiro ano mais de um ano, mas é para ser igual a PrdLtv_Grupo
    # portanto, pode ser removido!
    data_frame = data_frame.drop(columns="PrdLtv_Formatacao", errors='ignore')
    data_frame = data_frame.drop(columns="AcdHst_MdPrdLetivo", errors='ignore')
    data_frame = data_frame.drop(columns="AcdHst_NtExame", errors='ignore')
    data_frame = data_frame.drop(columns="TblGrlItm_CdgStcDscHistorico", errors='ignore')
    data_frame = data_frame.drop(columns="Dsc_Codigo", errors='ignore')
    data_frame = data_frame.drop(columns="Dsc_ChTotal", errors='ignore')
    data_frame = data_frame.drop(columns="AcdHst_GrdCrrCodigo", errors='ignore')
    data_frame = data_frame.drop(columns="PrdLtv_PrdLetivo", errors='ignore')
    data_frame = data_frame.drop(columns="TtlFaltas", errors='ignore')
    data_frame = data_frame.drop(columns="TblGrlItm_FrmOferta", errors='ignore')
    data_frame = data_frame.drop(columns="AcdHst_TpMatricula", errors='ignore')
    data_frame = data_frame.drop(columns="PrdLtv_GrpInicial", errors='ignore')
    data_frame = data_frame.drop(columns="TrfPrdLtvOrgCursados", errors='ignore')
    data_frame = data_frame.drop(columns="AnosContados", errors='ignore')
    data_frame = data_frame.drop(columns="TtlAnosCursados", errors='ignore')
    return data_frame


def remover_alunos_cursando(data_frame):
    # removendo alunos que estão cursando:
    # Selecione as linhas que atendem à condição e armazene seus índices em uma lista
    # substitua 'coluna' pelo nome da coluna e 'valor' pelo valor a ser buscado
    indices_a_remover = data_frame[data_frame['AcdStcAtualDescricao'] == 'Cursando'].index.tolist()
    # Remova as linhas selecionadas do DataFrame original
    data_frame = data_frame.drop(indices_a_remover)
    return data_frame


def remover_alunos_trancado(data_frame):
    indices_a_remover = data_frame[data_frame['AcdStcAtualDescricao'] == 'Trancado'].index.tolist()
    # Remova as linhas selecionadas do DataFrame original
    data_frame = data_frame.drop(indices_a_remover)
    return data_frame


def cria_colunas_disciplinas(data_frame):
    # Criando colunas para disciplinas:
    # usando o método pivot para transformar as informações de disciplinas e notas em colunas
    data_frame_pivot_disciplinas = data_frame.pivot(index='PssFsc_CdgAcademico', columns='Dsc_Descricao',
                                                    values='AcdHst_MdFinal').reset_index()
    data_frame_pivot_frequencia = data_frame.pivot(index='PssFsc_CdgAcademico', columns='Dsc_Descricao',
                                                   values='AcdHst_PrcFrequencia').reset_index()


    # data_frame_pivot_frequencia = data_frame_pivot_frequencia.dropna()
    # data_frame_pivot_disciplinas = data_frame_pivot_disciplinas.dropna()
    data_frame_pivot_disciplinas = data_frame_pivot_disciplinas.apply(pd.to_numeric, errors='coerce') #data_frame_pivot_disciplinas.astype(int)
    data_frame_pivot_frequencia = data_frame_pivot_frequencia.apply(pd.to_numeric, errors='coerce') #data_frame_pivot_frequencia.astype(int)


    # obter nomes atuais de todas as colunas do dataset
    nomes_colunas_frequencia = data_frame_pivot_frequencia.columns.tolist()
    nomes_colunas_frequencia.remove('PssFsc_CdgAcademico')
    # criar novo dicionário de nomes de colunas com sufixo
    new_columns = {}
    for col in nomes_colunas_frequencia:
        new_columns[col] = 'Frequencia_' + col
    # renomear as colunas do dataframe
    data_frame_pivot_frequencia = data_frame_pivot_frequencia.rename(columns=new_columns)

    # manter apenas as disciplinas de cálculo, computaçao 1 e álgebra:
    # data_frame_pivot = data_frame_pivot
    data_frame = pd.merge(data_frame, data_frame_pivot_disciplinas, left_on='PssFsc_CdgAcademico',
                          right_on='PssFsc_CdgAcademico')
    data_frame = pd.merge(data_frame, data_frame_pivot_frequencia, left_on='PssFsc_CdgAcademico',
                          right_on='PssFsc_CdgAcademico')
    data_frame = data_frame.drop_duplicates(subset='PssFsc_CdgAcademico', keep='first')
    data_frame = data_frame.drop(columns=['Dsc_Descricao', 'AcdHst_MdFinal', 'AcdHst_PrcFrequencia'])
    return data_frame

    # Pegga a primeira vez que a pessoa esteve na universidade.
    # Elimina matriculas duplicadass em disciplinas


def get_first_time_in_University(data_frame):
    # data_frame = data_frame.sort_values('PrdLetivoIng_Grupo', ascending=True)
    # data_frame = data_frame.drop_duplicates(subset=['PssFsc_CdgAcademico', 'Dsc_Descricao'], keep='first')
    # data_frame = data_frame.drop_duplicates(subset=['PssFsc_CdgAcademico', 'PrdLetivoIng_Grupo'], keep='first')

    data_frame = data_frame.sort_values(by=['PssFsc_CdgAcademico', 'PrdLetivoIng_Grupo'])  # classificar por ID e ano
    data_frame = data_frame.groupby('PssFsc_CdgAcademico').apply(
        lambda x: x[x['PrdLetivoIng_Grupo'] == x[
            'PrdLetivoIng_Grupo'].min()])  # selecionar as linhas com o ano mais antigo de cada ID
    data_frame = data_frame.droplevel(0)  # remover o nível de índice adicionado pelo groupby
    data_frame = data_frame.sort_values('PrdLetivoIng_Grupo', ascending=True)
    data_frame = data_frame.drop_duplicates(subset=['PssFsc_CdgAcademico', 'Dsc_Descricao'], keep='first')
    return data_frame


def get_first_time_1ano(data_frame):
    data_frame = data_frame[(data_frame['PrdLtv_Grupo'] == data_frame['PrdLetivoIng_Grupo']) &
                            (data_frame['AcdHst_GrdCrrSerie'] == 1)]
    # & (
    #                                 data_frame['TblGrlItm_DscStcHistorico'] == 'Ativa')]

    # Ordenar o DataFrame com base na coluna 'Situação' em ordem ascendente
    data_frame = data_frame.sort_values('TblGrlItm_DscStcHistorico', ascending=True)
    # Remover as duplicatas com base nas colunas 'ID' e 'Disciplina' e manter apenas a primeira ocorrência
    data_frame = data_frame.drop_duplicates(subset=['PssFsc_CdgAcademico', 'Dsc_Descricao'], keep='first')

    # # agora que pegou apenas o primeiro ano dá pra excluir a coluna do ano da disciplina:
    data_frame = data_frame.drop(columns="AcdHst_GrdCrrSerie", errors='ignore')
    data_frame = data_frame.drop(columns="TblGrlItm_DscStcHistorico", errors='ignore')
    data_frame = data_frame.drop(columns='PrdLtv_Grupo', errors='ignore')
    return data_frame


def cria_coluna_count_reprovacoes_primeiro_ano(data_frame):
    # data_frame['QtdDiscplinasReprovado'] = data_frame[data_frame['AcdHst_Resultado'] == 'Reprovado']['PssFsc_CdgAcademico'].value_counts()
    qtdDisciplinasReprovado = data_frame[data_frame['AcdHst_Resultado'] == 'Reprovado'][
        'PssFsc_CdgAcademico'].value_counts()
    print("Quantidade de disciplinas reprovado")
    print(qtdDisciplinasReprovado)
    data_frame.to_excel("../../dados_tcc_processados_python/GR 30_2018 antes de contar reprovações.xlsx", index=False)
    data_frame['QtdDiscplinasReprovado'] = data_frame['PssFsc_CdgAcademico'].map(qtdDisciplinasReprovado).fillna(0)
    data_frame = data_frame.drop(columns='AcdHst_Resultado')
    return data_frame


def set_idade_ingresso(data_frame):
    data_frame['Idade'] = data_frame['PrdLetivoIng_Grupo'] - data_frame['PssFsc_DtNascimento']
    data_frame = data_frame.drop(columns='PssFsc_DtNascimento')
    return data_frame


def cria_coluna_media_disciplinas(data_frame):
    # convertendo a coluna 'coluna1' para o tipo numérico
    data_frame['Computação I'] = pd.to_numeric(data_frame['Computação I'])
    data_frame['Cálculo Diferencial e Integral'] = pd.to_numeric(data_frame['Cálculo Diferencial e Integral'])
    data_frame['Geometria Analítica e Álgebra Linear'] = pd.to_numeric(
        data_frame['Geometria Analítica e Álgebra Linear'])
    data_frame['mediaDisciplinas'] = data_frame[
        ['Computação I', 'Cálculo Diferencial e Integral', 'Geometria Analítica e Álgebra Linear']].apply(
        lambda x: x.mean(), axis=1)
    return data_frame


def cria_coluna_DP_disciplinas(data_frame):
    data_frame['desvio_padrao-disciplinas'] = data_frame.apply(lambda row: np.std(
        row[['Computação I', 'Cálculo Diferencial e Integral', 'Geometria Analítica e Álgebra Linear']], ddof=1),
                                                               axis=1)
    #ddof = 1 desvio padrão da amostra, ddof = 0 desvio padrao populacao
    return data_frame


def remover_colunas_disciplinas_desnecessarias(data_frame):
    if 'Geometria e Álgebra' in data_frame:
        data_frame['Geometria Analítica e Álgebra Linear'] = \
            data_frame['Geometria Analítica e Álgebra Linear'].fillna(data_frame['Geometria e Álgebra'])
    if 'Frequencia_Geometria e Álgebra' in data_frame:
        data_frame['Frequencia_Geometria Analítica e Álgebra Linear'] = \
            data_frame['Frequencia_Geometria Analítica e Álgebra Linear'].fillna(
            data_frame['Frequencia_Geometria e Álgebra'])
    # criar lista de substrings a serem buscadas nos rótulos das colunas
    substrings = ['Introdução à Administração', 'Física', 'Inglês', 'Introdução', 'Lógica', 'Metodologia',
                  'Probabilidade', 'Prática',
                  'Sociologia', 'Técnicas', 'Geometria e Álgebra']
    # selecionar colunas cujos rótulos contêm alguma das substrings da lista
    colunas_selecionadas = data_frame.filter(regex='|'.join(substrings))
    # remover colunas selecionadas
    data_frame = data_frame.drop(columns=colunas_selecionadas.columns)
    return data_frame


def remover_alunos_jubilado(data_frame):
    indices_a_remover = data_frame[data_frame['AcdStcAtualDescricao'] == 'Jubilado'].index.tolist()
    # Remova as linhas selecionadas do DataFrame original
    data_frame = data_frame.drop(indices_a_remover)
    return data_frame



def rotular_situacao(data_frame: DataFrame):
    valores_coluna_target = data_frame['AcdStcAtualDescricao'].unique()
    for value in valores_coluna_target:
        if value == 'Formado':
            data_frame.loc[data_frame['AcdStcAtualDescricao'] == value, 'AcdStcAtualDescricao'] = "Formado"
        elif value == 'Cursando':
            data_frame.loc[data_frame['AcdStcAtualDescricao'] == value, 'AcdStcAtualDescricao'] = "Cursando"
        elif value == 'Trancado':#não precisa fazer nada
            data_frame.loc[data_frame['AcdStcAtualDescricao'] == value, 'AcdStcAtualDescricao'] = "Trancado"
        else:
            data_frame.loc[data_frame['AcdStcAtualDescricao'] == value, 'AcdStcAtualDescricao'] = "Evadido"
    return data_frame

def rotular_municipio_procedencia(data_frame: DataFrame):
    valores_coluna_target = data_frame['EndMnc_Descricao'].unique()
    for value in valores_coluna_target:
        if value == 'Foz do Iguaçu' or value == 'Santa Terezinha de Itaipu':
            data_frame.loc[data_frame['EndMnc_Descricao'] == value, 'EndMnc_Descricao'] = "Dentro da Região de Foz"
        else:
            data_frame.loc[data_frame['EndMnc_Descricao'] == value, 'EndMnc_Descricao'] = "Fora da Região de Foz"
    return data_frame

def rotular_dados_colunas(data_frame: DataFrame):
    data_frame = rotular_situacao(data_frame)
    data_frame = rotular_municipio_procedencia(data_frame)
    return data_frame


def get_dataframe_gr30(file_gr30='../../dadosTCC/GR 30_2018 _com ID.xlsx',
                       file_gr73='../../dadosTCC/GR 73_até2018_com ID.xlsx',
                       file_gr02='../../dadosTCC/GR 02_Fabiana Frata_ref_completa.xlsx', is_training_data=True):
    print("Olá bom dia datasetgr30!")
    # REalizando a leitura do arquivo excel com os dados:
    base = '../../dadosTCC/'
    nome_arquivo_base_dados = base + 'GR 30_2018 _com ID.xlsx'
    nome_arquivo_base_dados = file_gr30

    data_frame = pd.read_excel(nome_arquivo_base_dados, 'Planilha1')
    data_frame_gr73 = get_dataframe_gr73(file_gr73, file_gr02, is_training_data)

    info_file_data(data_frame)
    data_frame = basic_processing(data_frame)
    data_frame = remover_colunas_desnecessarias(data_frame)
    if is_training_data:
        data_frame = remover_alunos_cursando(data_frame)
        data_frame = remover_alunos_trancado(data_frame)
    data_frame = remover_alunos_jubilado(data_frame)

    # Será utilizado para calcular a idade do academico.:
    # data_frame = data_frame.drop(columns="PrdLetivoIng_Grupo")

    # Remove todas as colunas que a quantidade de dados faltantes é maior que 30% do total de entradas ou vazias:
    data_frame = data_frame.dropna(axis=1, thresh=(get_data_frame_size(data_frame) * 0.7))
    # agora é possível apagar as linhas que faltam dados:
    data_frame = data_frame.dropna()
    data_frame = rotular_resultado_disciplinas(data_frame)
    # Pegar apenas a primeira vez que a pessoa cursou as disciplinas do primeiro ano:
    data_frame = get_first_time_1ano(data_frame)
    # Pega apenas a primeira ocorrencia na univesidade de acordo com o ano:
    data_frame = get_first_time_in_University(data_frame)
    # Criando coluna com  o número de reprovaçoes do aluno:
    data_frame = cria_coluna_count_reprovacoes_primeiro_ano(data_frame)
    # Criando colunas para disciplinas:
    data_frame = cria_colunas_disciplinas(data_frame)
    # juntando os dados de caracterização(gr73 e gr02) com os de desempenho (gr30)
    data_frame = merge_gr30_gr73(data_frame, data_frame_gr73)
    data_frame = data_frame.drop(columns='TGIStcAtualDescricao', errors='ignore')
    data_frame = set_idade_ingresso(data_frame)
    data_frame = remover_colunas_disciplinas_desnecessarias(data_frame)
    data_frame = data_frame.drop(columns='PrdLetivoIng_Grupo', errors='ignore')
    # remove todas as linhas que possuem dados faltantes:
    data_frame = data_frame.dropna()

    data_frame = cria_coluna_media_disciplinas(data_frame)
    data_frame = cria_coluna_DP_disciplinas(data_frame)
    # remove outliers com idades inconsistentes:
    data_frame = data_frame[data_frame['Idade'] > 15]
    print(data_frame['AcdStcAtualDescricao'].value_counts())

    #ajusta os rótulos das colunas e padroniza as descrições:
    data_frame = rotular_dados_colunas(data_frame)


    data_frame.to_excel("../../dados_tcc_processados_python/GR 30_2018_com ID processado sem codificar.xlsx",
                        index=False)

    #codificar dados do dataframe:

    # valores_coluna_target = data_frame['AcdStcAtualDescricao'].unique()
    # rever isso, esse codigo comentadno apenas codifica a variável algo!
    # for value in valores_coluna_target:
    #     if value == 'Formado':
    #         data_frame.loc[data_frame['AcdStcAtualDescricao'] == value, 'AcdStcAtualDescricao'] = 0
    #     else:
    #         data_frame.loc[data_frame['AcdStcAtualDescricao'] == value, 'AcdStcAtualDescricao'] = 1

    # data_frame, codificadores  = codificar_dados(data_frame)
    # # Salvar os codificadores
    # salvar_codificadores(codificadores, '../../files/codificadores.json')
    #
    # data_frame.to_excel("../../dados_tcc_processados_python/GR 30_2018 _com ID processado codificado.xlsx", index=False)
    #
    # # Carregar os codificadores
    # codificadores_carregados = carregar_codificadores('../../files/codificadores.json')
    #
    # # Decodificar os dados
    # dataset_decodificado = decodificar_dados(data_frame, codificadores_carregados)
    # dataset_decodificado.to_excel("../../dados_tcc_processados_python/GR 30_2018 _com ID processado descodificado.xlsx", index=False)
    #
    # dataset_decodificado = codificar_dataframe(dataset_decodificado,codificadores_carregados)
    #
    # # Carregar os codificadores
    # codificadores_carregados = carregar_codificadores('../../files/codificadores.json')
    #
    # # Decodificar os dados
    # dataset_decodificado = decodificar_dados(data_frame, codificadores_carregados)
    #
    # return dataset_decodificado
    return data_frame

    # codificando os valores da variável target para evadido(1) não evadido (0)
    # Obtenção dos valores discretos da coluna
    valores_coluna_target = data_frame['AcdStcAtualDescricao'].unique()

    for value in valores_coluna_target:
        if value == 'Formado':
            data_frame.loc[data_frame['AcdStcAtualDescricao'] == value, 'AcdStcAtualDescricao'] = 0
        else:
            data_frame.loc[data_frame['AcdStcAtualDescricao'] == value, 'AcdStcAtualDescricao'] = 1

    # Aplicando Label Encoding para converter valores categóricos (discretos) em números
    # Selecionar apenas as colunas do tipo 'object'
    obj_cols = data_frame.select_dtypes(include=['object']).columns
    # Aplicar o Label Encoding em cada coluna selecionada
    for col in obj_cols:
        le = LabelEncoder()
        data_frame[col] = le.fit_transform(data_frame[col])

    # tabelas:
    print(data_frame.info())
    data_frame.to_excel("../../dados_tcc_processados_python/GR 30_2018 _com ID processado codificado.xlsx", index=False)
    return data_frame


if __name__ == '__main__':
    get_dataframe_gr30()
