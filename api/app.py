from doctest import debug
from random import Random
from flask import Flask, request, jsonify, json
from flask_cors import CORS
from pandas import DataFrame
from src.algoritmos.modelo import predict
from src.pre_processamento_dados.pre_processamento_GR_30 import get_dataframe_gr30
from src.uttil.constants import colunasTabelaClassificacao, chart_types
app = Flask(__name__)
CORS(app)


data_frame = DataFrame()

@app.route('/upload', methods=['POST'])
def upload_files():
    global data_frame
    # Obtém os arquivos enviados pelo formulário
    files = request.files.getlist('files')
    file_gr30 = 0
    file_gr73 = 0
    file_gr02 = 0
    file_gr02 = request.files.get('fileGR02')
    file_gr73 = request.files.get('fileGR73')
    file_gr30 = request.files.get('fileGR30')

    # for file in files:
    #     print(file.filename)
    #     if file.filename == 'GR 30_apenas_2018.xlsx' or file.filename == 'GR 30_2018 _com ID.xlsx':
    #         file_gr30 = file
    #     elif file.filename == 'GR 73_até2018_com ID.xlsx':
    #         file_gr73 = file
    #     else:
    #         file_gr02 = file
    data_frame = get_dataframe_gr30(file_gr30, file_gr73, file_gr02, False)
    resultado = jsonify(data_frame.to_dict())
    return resultado


@app.route('/dataset', methods=['GET'])
def get_data_frame():
    global data_frame
    data_frame_predito = predict(data_frame)
    data_frame_resumido = data_frame_predito[colunasTabelaClassificacao]
    data_frame_resumido = data_frame_predito.reindex(columns=colunasTabelaClassificacao)
    print(data_frame_resumido.to_json(orient='records'))
    resultado = jsonify(data_frame_resumido.to_dict(orient='records'))
    print(resultado.data)
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
    print(data_frame.columns)
    # chart_types = {
    #     'Forma de Ingresso': 'pie',
    #     'Situação': 'pie',
    #     'NúmeroDisciplinasReprovado1ºano': 'bar',
    #     'Sexo': 'pie',
    #     'Endereço': 'pie',
    #     'TipoInstituiçãoDeOrigem': 'pie',
    #     'Idade': 'bar',
    #     'Cotista': 'pie',
    #     'Cor': 'pie',
    #
    #     # Adicione outras colunas e tipos de gráfico conforme necessário
    # }



    # Obtenha os dados e opções dos gráficos
    chart_data_list = []

    #for column in data_frame.columns:
    for column, chart_type in chart_types.items():
        # Conte a ocorrência de cada valor na coluna
        contagem_valores = data_frame[column].value_counts()
        #contagem_valores = column.value_counts()
        valores = contagem_valores.values.tolist()
        rotulos = contagem_valores.index.tolist()

        # Obtenha a quantidade de dados diferentes na coluna 'coluna'
        num_values = data_frame[column].nunique()
        if chart_type == 'bar':
            num_values = 1
        # Gerar um array de cores aleatórias com base na quantidade de valores
       # num_values = 3  # Altere para a quantidade de valores no seu gráfico
        colors = [random_color() for _ in range(num_values)]

        chart_data = {
            "type": chart_type,
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
                'maintainAspectRatio': False,

                'plugins': {
                    'legend': {
                        'position': 'right',
                    },
                    'title': {
                        'display': 'true',
                        'text': column,
                    },
                    'datalabels': {
                        'display': 'true',
                        'color': 'white',
                        'font': {
                            'weight': 'bold'
                        },
                        'formatter': 'function(value, context) { return value + "%"; }'
                    }

                },



            },
        }
        chart_data_list.append(chart_data)

    # Retorne os dados e opções como resposta JSON
    return json.dumps(chart_data_list)


@app.route('/')
def index():
    return 'Hello World'


if __name__ == '__main__':
    app.run(debug=True)

