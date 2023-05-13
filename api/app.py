from doctest import debug

from flask import Flask, request
from flask_cors import CORS

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

    # Processa os arquivos e devolve um resultado
    resultado = 'Deu tudo certo!'

    return resultado


@app.route('/')
def index():
    return 'Hello World'


if __name__ == '__main__':
    app.run(debug=True)

