from flask import Flask
from controllers.NotaController import nota
from controllers.AvaliacaoController import avaliacao

app = Flask(__name__)

app.register_blueprint(nota)
app.register_blueprint(avaliacao)

app.run(port=8080,debug=True)