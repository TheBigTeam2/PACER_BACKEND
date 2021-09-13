# Modules
import mariadb
from dataclasses import dataclass
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@127.0.0.1:3306/PACER"

db = SQLAlchemy(app)

#CLASSES e Tabelas

class Nota(db.Model):
    not_id = db.Column(db.BigInteger, primary_key=True)
    not_avaliacao = db.Column(db.BigInteger)
    not_criterio = db.Column(db.String(32), nullable=False)
    not_valor = db.Column(db.BigInteger, nullable=False)

@dataclass
class Avaliacao(db.Model):
    ava_id: int
    ava_sprint: int
    ava_inicio: str
    ava_termino: str
    ava_avaliado: int
    ava_avaliador: int
    ava_projeto: int
    
    ava_id = db.Column(db.BigInteger, primary_key=True)
    ava_sprint = db.Column(db.Integer, nullable=False)
    ava_inicio = db.Column(db.Date, nullable=False)
    ava_termino = db.Column(db.Date, nullable=False)
    ava_avaliado = db.Column(db.BigInteger)
    ava_avaliador = db.Column(db.BigInteger)
    ava_projeto = db.Column(db.BigInteger)

@dataclass
class Usuario(db.Model):
    usu_id: int
    usu_nome: str
    
    usu_id = db.Column(db.BigInteger, primary_key=True)
    usu_nome = db.Column(db.String(128))

@dataclass
class Projeto(db.Model):
    pro_id: int
    pro_equipe: int
    
    pro_id = db.Column(db.BigInteger, primary_key=True)
    pro_equipe = db.Column(db.BigInteger)

@dataclass
class Projeto_Equipe(db.Model):
    pre_projeto: int
    pre_equipe: int
    
    pre_projeto = db.Column(db.BigInteger, primary_key=True)
    pre_equipe = db.Column(db.BigInteger, primary_key=True)

@dataclass
class Equipe(db.Model):
    equ_id: int
    equ_nome: str
    equ_disciplina: int
    
    equ_id = db.Column(db.BigInteger, primary_key=True)
    equ_nome = db.Column(db.String(128))
    equ_disciplina = db.Column(db.BigInteger)

@dataclass
class Aluno_Equipe(db.Model):
    ale_aluno: int
    ale_equipe: int
    
    ale_aluno = db.Column(db.BigInteger, primary_key=True)
    ale_equipe = db.Column(db.BigInteger, primary_key=True)

@dataclass
class Aluno(db.Model):
    alu_id: int
    alu_ra: int
    alu_usuario: int
    
    alu_id = db.Column(db.BigInteger, primary_key=True)
    alu_ra = db.Column(db.BigInteger)
    alu_usuario = db.Column(db.BigInteger)

@app.route('/nota', methods=['POST', 'GET'])
def inserir_notas():

    # POST das notas:
    if request.method == 'POST':
        
        notas = request.get_json()

        for nota in notas:
            ava = nota['avaliacao']
            cri = nota['criterio']
            n = nota['nota']
            try:
                insercao = Nota(not_avaliacao = ava, not_criterio = cri, not_valor = n)
                db.session.add(insercao)
                db.session.commit()
            except Exception as e:
                print("Não foi possivel adicionar")
                print(e)
            
    # GET das avaliações:
    if request.method == 'GET':
        avaliacoes = Avaliacao.query.all()
        return jsonify(avaliacoes)

@app.route('/avaliacao', methods=['POST', 'GET'])
def avaliacao():

    # POST da avaliacao:
    if request.method == 'POST':
        
        avaliacoes = request.get_json()

        for ava in avaliacoes:
            sprint = ava['sprint']
            inicio = ava['inicio']
            termino = ava['termino']
            avaliado = ava['avaliado']
            avaliador = ava['avaliador']
            projeto = ava['projeto']
            try:
                insercao = Avaliacao(ava_sprint = sprint, ava_inicio = inicio, ava_termino = termino, ava_avaliado = avaliado, ava_avaliador = avaliador, ava_projeto = projeto)
                db.session.add(insercao)
                db.session.commit()
            except Exception as e:
                print("Não foi possivel adicionar")
                print(e)
            
    # GET dos membros da equipe:
    if request.method == 'GET':
        
    


if __name__ == '__main__':

    #inserir_notas()
    app.debug = True
    app.run()
