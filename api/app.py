from doctest import debug
from random import Random

from flask import Flask, request, jsonify, json
from flask_cors import CORS
import pandas as pd
import requests
from pandas import DataFrame

from src.pre_processamento_dados.codificacao import codificar_dataframe, codificar_dados, codificar_instancia, \
    carregar_codificadores
from src.pre_processamento_dados.codificar_dados import decodificar_dados, carregar_codificadores, codificar_dataframe, \
    salvar_codificadores, codificar_dados
from src.pre_processamento_dados.pre_processamento_GR_30 import get_dataframe_gr30

app = Flask(__name__)
CORS(app)

# @app.route('/upload', methods=['POST'])
# def upload_files():
#     arquivos = request.files.getlist('arquivos_dados_alunos')
#     # Faça algo com os arquivos aqui
#     return 'Arquivos enviados com sucesso!'

data_frame = DataFrame()

@app.route('/upload', methods=['POST'])
def upload_files():
    global data_frame
    # Obtém os arquivos enviados pelo formulário
    files = request.files.getlist('files')
    file_gr30 = 0
    file_gr73 = 0
    file_gr02 = 0
    for file in files:
        print(file.filename)
        if file.filename == 'GR 30_apenas_2018.xlsx' or file.filename == 'GR 30_2018 _com ID.xlsx':
            file_gr30 = file
        elif file.filename == 'GR 73_até2018_com ID.xlsx':
            file_gr73 = file
        else:
            file_gr02 = file
    data_frame = get_dataframe_gr30(file_gr30, file_gr73, file_gr02, False)
    # Processa os arquivos e devolve um resultado
    resultado = 'Deu tudo certo!'
    resultado = jsonify(data_frame.to_dict())
    return resultado


@app.route('/dataset', methods=['GET'])
def get_data_frame():
    global data_frame
    resultado = jsonify(data_frame.to_dict(orient='records'))
    return resultado


def random_color():
    random = Random()
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    #color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
    color = f'rgb({r}, {g}, {b})'
    return color


@app.route('/dados_grafico', methods=['GET'])
def get_dados_grafico():
    global data_frame
    # Codificar os dados do DataFrame
    data_frame_codificado, codificadores = codificar_dados(data_frame)

    # Salvar os codificadores em um arquivo
    salvar_codificadores(codificadores, 'codificadores.pkl')

    codificadores = carregar_codificadores('codificadores.pkl')
    # Decodificar os dados do DataFrame codificado
    data_frame_decodificado = decodificar_dados(data_frame_codificado, codificadores)
    data_frame = data_frame_decodificado

    data_frame = codificar_dataframe(data_frame,codificadores)

    # Obtenha os dados e opções dos gráficos
    chart_data_list = []

    for column in data_frame.columns:
        # Conte a ocorrência de cada valor na coluna
        contagem_valores = data_frame[column].value_counts()
        #contagem_valores = column.value_counts()
        valores = contagem_valores.values.tolist()
        rotulos = contagem_valores.index.tolist()

        # Obtenha a quantidade de dados diferentes na coluna 'coluna'
        num_values = data_frame[column].nunique()
        # Gerar um array de cores aleatórias com base na quantidade de valores
       # num_values = 3  # Altere para a quantidade de valores no seu gráfico
        colors = [random_color() for _ in range(num_values)]

        chart_data = {
            "type": "pie",
            'data': {
                'labels': rotulos,
                'datasets': [
                    {
                        'label': column,
                        'data': valores,
                        'backgroundColor': colors
                    }
                ]
            },
            'options': {
                'responsive': True,
                'maintainAspectRatio': False
            }
        }
        chart_data_list.append(chart_data)

    # Retorne os dados e opções como resposta JSON
    return json.dumps(chart_data_list)


@app.route('/')
def index():
    return 'Hello World'


if __name__ == '__main__':
    app.run(debug=True)

