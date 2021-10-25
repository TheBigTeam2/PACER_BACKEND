from flask import Flask
from controllers.NotaController import nota
from controllers.EquipeController import equipe
from controllers.UsuarioController import usuario
from controllers.AvaliacaoController import avaliacao
from controllers.CriterioController import criterio

app = Flask(__name__)

app.register_blueprint(nota)
app.register_blueprint(equipe)
app.register_blueprint(usuario)
app.register_blueprint(avaliacao)
app.register_blueprint(criterio)

app.run(port=8085,debug=True)