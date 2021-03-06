from flask import Flask
from flask_cors import CORS
from controllers.NotaController import nota
from controllers.EquipeController import equipe
from controllers.UsuarioController import usuario
from controllers.AvaliacaoController import avaliacao
from controllers.CriterioController import criterio
from controllers.ProjetoController import projeto
from controllers.DisciplinaController import disciplina
from controllers.AutenticacaoController import autenticacao
from controllers.LogsController import logs

app = Flask(__name__)
CORS(app)

app.register_blueprint(nota)
app.register_blueprint(equipe)
app.register_blueprint(usuario)
app.register_blueprint(avaliacao)
app.register_blueprint(criterio)
app.register_blueprint(projeto)
app.register_blueprint(disciplina)
app.register_blueprint(autenticacao)
app.register_blueprint(logs)

app.run(port=8085,debug=True)