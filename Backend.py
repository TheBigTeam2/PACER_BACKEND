# Modules
import mariadb
import json
from dataclasses import dataclass
import dataclasses
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, create_engine
from sqlalchemy.orm import sessionmaker
import sys

app = Flask(__name__)
CORS(app)
path = "mysql+pymysql://root:root@127.0.0.1:3306/PACER"

app.config["SQLALCHEMY_DATABASE_URI"] = path

'''
#Abrir Sessão:
engine = create_engine(path)
Session = sessionmaker(engine)
session = Session()
'''

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

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

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

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

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

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

def buscar_alunos(proj):
    equ = []
    alu = []
    a = []
    p = select(Projeto_Equipe.pre_equipe).where(Projeto_Equipe.pre_projeto == proj)
    for row in db.session.execute(p):
        equ.append(row[0])

    for e in equ:
        alu = []
        q = select(Aluno_Equipe.ale_aluno).where(Aluno_Equipe.ale_equipe == e)
        for row in db.session.execute(q):
            alu.append(row[0])
        a.append(alu)
    return a

'''
def buscar_ava():
    proj = Projeto.query.all()
    usuario = '7'
    for p in proj:
        j = p.as_dict()
        j.pop('pro_equipe')
        print(j)
'''
        
@app.route('/aluno/<string:id>/nota', methods=['POST', 'GET'])
def inserir_notas(id):

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
        avaliacoes = []
        ava = Avaliacao.query.filter(Avaliacao.ava_avaliador == id).all()
        for a in ava:
            avaliacoes.append(a.as_dict())
        return jsonify(avaliacoes)

@app.route('/professor/<string:id>/avaliacao', methods=['POST', 'GET'])
def avaliacao(id):

    # POST da avaliacao:
    if request.method == 'POST':
        avaliacoes = request.get_json()
        
        sprint = avaliacoes['sprint']
        inicio = avaliacoes['inicio']
        termino = avaliacoes['termino']
        projeto = avaliacoes['projeto']

        alunos = []
        alunos = buscar_alunos(projeto)
            
        for aluno in alunos:
            i = 0
            print(aluno)
            while i < len(aluno):
                try:
                    #Avalia a si próprio:
                    avaliador = aluno[i]
                    insercao_proprio = Avaliacao(ava_sprint = sprint, ava_inicio = inicio, ava_termino = termino, ava_avaliado = avaliador, ava_avaliador = avaliador, ava_projeto = projeto)
                        
                    #Avalia um colega de equipe:
                    avaliado = aluno[(i + 1) % len(aluno)]
                    insercao_colega1 = Avaliacao(ava_sprint = sprint, ava_inicio = inicio, ava_termino = termino, ava_avaliado = avaliado, ava_avaliador = avaliador, ava_projeto = projeto)
                        
                    #Avalia outro colega de equipe:
                    avaliado = aluno[(i + 2) % len(aluno)]
                    insercao_colega2 = Avaliacao(ava_sprint = sprint, ava_inicio = inicio, ava_termino = termino, ava_avaliado = avaliado, ava_avaliador = avaliador, ava_projeto = projeto)

                    db.session.add(insercao_proprio)
                    db.session.add(insercao_colega1)
                    db.session.add(insercao_colega2)
                    db.session.commit()
                    i += 1
                except Exception as e:
                        print("Não foi possivel adicionar")
                        print(e)
            
    # GET dos membros da equipe:
    if request.method == 'GET':
        projetos = []
        proj = Projeto.query.all()
        for pr in proj:
            p = pr.as_dict()
            p.pop('pro_equipe')
            projetos.append(p)
        return jsonify(projetos)

if __name__ == '__main__':
    
    app.debug = True
    app.run()
