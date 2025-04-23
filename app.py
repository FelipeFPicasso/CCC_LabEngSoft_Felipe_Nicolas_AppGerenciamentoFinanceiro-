from flask import Flask

app = Flask(__name__)

@app.route('hello')
def hello():
    return 'Esse é um app de gerenciamento financeiro'

if __name__ == '__main__':
    app.run(debug = True, port=8000, host = '0.0.0.0')