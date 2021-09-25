from flask import Flask
from controllers.NotaController import nota

app = Flask(__name__)

app.register_blueprint(nota)

app.run(port=8080)