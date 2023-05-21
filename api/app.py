from doctest import debug

from flask import Flask, request
from flask_cors import CORS
import pandas as pd

from src.pre_processamento_dados.pre_processamento_GR_30 import get_dataframe_gr30

app = Flask(__name__)
CORS(app)

# @app.route('/upload', methods=['POST'])
# def upload_files():
#     arquivos = request.files.getlist('arquivos_dados_alunos')
#     # Faça algo com os arquivos aqui
#     return 'Arquivos enviados com sucesso!'


@app.route('/upload', methods=['POST'])
def upload_files():
    # Obtém os arquivos enviados pelo formulário
    files = request.files.getlist('files')
    file_gr30 = 0
    file_gr73 = 0
    file_gr02 = 0
    for file in files:
        print(file.filename)
        if file.filename == 'GR 30_apenas_2018.xlsx':
            file_gr30 = file
        elif file.filename == 'GR 73_até2018_com ID.xlsx':
            file_gr73 = file
        else:
            file_gr02 = file
        data_frame = pd.read_excel(file, 'Planilha1')
        data_frame.info()
    # data_frame = get_dataframe_gr30(file_gr30, file_gr73, file_gr02)
    # print(data_frame.info())
    # Processa os arquivos e devolve um resultado
    resultado = 'Deu tudo certo!'

    return resultado


@app.route('/')
def index():
    return 'Hello World'


if __name__ == '__main__':
    app.run(debug=True)

