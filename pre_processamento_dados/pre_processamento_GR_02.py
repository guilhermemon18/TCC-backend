import pandas as pd



def get_dataframe_gr02_necessary_columns():
    # REalizando a leitura do arquivo excel com os dados:
    base = '../../dadosTCC/'
    nome_arquivo_base_dados = base + 'GR 02_Fabiana Frata_ref_completa.xlsx'
    data_frame = pd.read_excel(nome_arquivo_base_dados, 'Planilha1')
    data_frame = data_frame.drop_duplicates()
    # Mantenha apenas as colunas necessárias:
    colunas_manter = ['PssFsc_Codigo', 'PssFsc_DtNascimento', 'PssFsc_Sexo']
    data_frame = data_frame[colunas_manter]
    data_frame['PssFsc_DtNascimento'] = pd.to_datetime(data_frame['PssFsc_DtNascimento']).dt.year
    # Renomeie a coluna "Idade" para "Anos"
    #data_frame = data_frame.rename(columns={'PssFsc_DtNascimento': 'AnoNascimento'})
    return data_frame

def get_dataframe_gr_02():
    #REalizando a leitura do arquivo excel com os dados:
    base = '../dadosTCC/'
    nome_arquivo_base_dados = base + 'GR 02_Fabiana Frata_ref_completa.xlsx'
    data_frame = pd.read_excel(nome_arquivo_base_dados, 'Planilha1')
    #Terminando a leitura e guardando-os na variável data_frame.

    #imprimindo a quantidade de dados no dataset
    print('quantidade de dados no data_frame')
    data_frame_size = len(data_frame.index)
    print(data_frame_size)

    #Imprimindo a quantidade de valores nulos (em branco) e valores totais do dataframe
    print("Quantidade de dados em cada coluna:")
    print(data_frame.count())
    print()
    print("Quantidade de dado NULOS em cada coluna: ")
    print(data_frame.isnull().sum().sort_values(ascending=False)[:10])
    print()

    #Realizando pré_processamento nos dados:
    #Removendo linhas duplicadas (básico)
    data_frame = data_frame.drop_duplicates()
    #Remove todas as colunas que a quantidade de dados faltantes é maior que 10% do total de entradas e vazias:
    data_frame = data_frame.dropna(axis=1, thresh=(data_frame_size * 0.7))

    #Deletando a coluna com o RA do aluno, pois é irrelevante!
    data_frame = data_frame.drop(columns="PssFsc_Codigo")

    #deletando colunas em que todos os dados são iguais
    # Obtendo as colunas com apenas um valor
    colunas_remover = data_frame.columns[data_frame.nunique() == 1]
    # Removendo as colunas com apenas um valor
    data_frame = data_frame.drop(colunas_remover, axis=1)

    #Deletando colunas em que os dados são todos o mesmo valor CFOZ  e Campus de Foz do Iguaçu
    #data_frame = data_frame.drop(columns="CdgCampus_Polo")
    #data_frame = data_frame.drop(columns="DscCampus_Polo")

    #Deletando a coluna que todos os números são iguais, são 1.
    data_frame = data_frame.drop(columns="TpEnd_Codigo")


    #imprimindo a quantidade de dados no dataset
    print('quantidade de dados no data_frame')
    data_frame_size = len(data_frame.index)
    print(data_frame_size)

    #Imprimindo a quantidade de valores nulos (em branco) e valores totais do dataframe
    print("Quantidade de dados em cada coluna:")
    print(data_frame.count())
    print()
    print("Quantidade de dado NULOS em cada coluna: ")
    print(data_frame.isnull().sum().sort_values(ascending=False)[:10])
    print()

    # tabelas:
    print(data_frame.info())
    print(data_frame.describe())


