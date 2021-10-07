from flask import Flask
from controllers.NotaController import nota
from controllers.AvaliacaoController import avaliacao
from controllers.UsuarioController import usuario

app = Flask(__name__)

app.register_blueprint(nota)
app.register_blueprint(avaliacao)
app.register_blueprint(usuario)

app.run(port=5000,debug=True)