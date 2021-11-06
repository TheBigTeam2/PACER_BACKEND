from flask import Flask
from flask_cors import CORS
from controllers.NotaController import nota
from controllers.EquipeController import equipe
from controllers.UsuarioController import usuario
from controllers.AvaliacaoController import avaliacao
from controllers.CriterioController import criterio
from controllers.AlunoEquipeController import alunoequipe

app = Flask(__name__)
CORS(app)

app.register_blueprint(nota)
app.register_blueprint(equipe)
app.register_blueprint(usuario)
app.register_blueprint(avaliacao)
app.register_blueprint(criterio)
app.register_blueprint(alunoequipe)

app.run(port=8085,debug=True)