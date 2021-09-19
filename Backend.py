# Modules
import mariadb
import json
from dataclasses import dataclass
import dataclasses
from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import sys

app = Flask(__name__)
CORS(app)
path = "mysql+pymysql://[username]:[password]@[ip]:[port]/PACER"

app.config["SQLALCHEMY_DATABASE_URI"] = path

db = SQLAlchemy(app)

#CLASSES e Tabelas

class Nota(db.Model):
    not_id = db.Column(db.BigInteger, primary_key=True)
    not_avaliacao = db.Column(db.BigInteger)
    not_criterio = db.Column(db.String(32), nullable=False)
    not_valor = db.Column(db.BigInteger, nullable=False)

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

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
class Projeto_equipe(db.Model):
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
class Aluno_equipe(db.Model):
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

@dataclass
class Disciplina(db.Model):
    dis_id: int
    dis_semestre: str
    dis_professor: str
    dis_nome: str
    
    dis_id = db.Column(db.BigInteger, primary_key=True)
    dis_semestre = db.Column(db.String(32), nullable=False)
    dis_professor = db.Column(db.BigInteger)
    dis_nome = db.Column(db.String(64), nullable=False)

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
    
@dataclass
class Disciplina_projeto(db.Model):
    dip_disciplina: int
    dip_projeto: int

    dip_disciplina = db.Column(db.BigInteger, primary_key=True)
    dip_projeto = db.Column(db.BigInteger, primary_key=True)

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

#Realizar Busca de Alunos que fazem parte do projeto:
def buscar_alunos(proj):
    equ = []
    alu = []
    a = []
    p = select(Projeto_equipe.pre_equipe).where(Projeto_equipe.pre_projeto == proj)
    for row in db.session.execute(p):
        equ.append(row[0])

    for e in equ:
        alu = []
        q = select(Aluno_equipe.ale_aluno).where(Aluno_equipe.ale_equipe == e)
        for row in db.session.execute(q):
            alu.append(row[0])
        a.append(alu)
    return a

#Buscar Projetos que o Professor faz parte:
def buscar_projetos(professor):
    projetos = []
    proj = []
    disciplina = []
    disciplinas = select(Disciplina.dis_id).where(Disciplina.dis_professor == professor)
    for row in db.session.execute(disciplinas):
        disciplina.append(row[0])
    for discip in disciplina:
        dis = Disciplina_projeto.query.filter(Disciplina_projeto.dip_disciplina == discip).with_entities(Disciplina_projeto.dip_projeto).all()
        for d in dis:
            proj.append(d[0])
    for p in proj:
        ava = Avaliacao.query.filter(Avaliacao.ava_projeto == p).with_entities(Avaliacao.ava_id, Avaliacao.ava_sprint, Avaliacao.ava_avaliador, Avaliacao.ava_avaliado).all()
        avaliacoes = []
        for av in ava:
            notasBruto = Nota.query.filter(Nota.not_avaliacao == av[0]).with_entities(Nota.not_valor, Nota.not_criterio).all()
            notas = []
            for nota in notasBruto:
                notas.append({
                        "criterio": nota[0],
                        "valor": nota[1]
                    })
            avaliacoes.append({
                    "id": av[0],
                    "sprint": av[1],
                    "avaliador": av[3],
                    "avaliado": av[2],
                    "equipe": 'null',
                    "notas": notas
                })
        projetos.append({
            "id": p,
            "avaliacoes": avaliacoes
        })
    print(projetos)
    return projetos
        
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
        resp = []
        avaliacoes = request.get_json()
        
        sprint = avaliacoes['sprint']
        inicio = avaliacoes['inicio']
        termino = avaliacoes['termino']
        projeto = avaliacoes['projeto']

        alunos = []
        alunos = buscar_alunos(projeto)
            
        for aluno in alunos:
            i = 0
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
                        return (e)
        ava = Avaliacao.query.filter(Avaliacao.ava_sprint == sprint, Avaliacao.ava_inicio == inicio, Avaliacao.ava_termino == termino, Avaliacao.ava_projeto == projeto).all()
        for a in ava:
            resp.append(a.as_dict())
        return jsonify(resp), 200
            
    # GET dos membros da equipe:
    if request.method == 'GET':
        projetos = []
        projetos = buscar_projetos(id)
        return jsonify(projetos)

@app.post('/avaliacao/abrir')
def open_avalitation():
    response = make_response()
    response.status_code = 201

    try:
        body = request.get_json()

        avaliacao = Avaliacao(
            ava_sprint = body.get('ava_sprint'),
            ava_inicio = body.get('ava_inicio'),
            ava_termino = body.get('ava_termino'),
            ava_avaliado = body.get('ava_avaliado'),
            ava_avaliador = body.get('ava_avaliador'),
            ava_projeto = body.get('ava_projeto')
        )

        db.session.add(avaliacao)
        db.session.commit()

        response.status_code = 201

        return jsonify({"content":avaliacao.as_dict()})

    except Exception as e:
        response.status_code = 500
        raise e

@app.post('/avaliacao/fechar')
def close_avaliation():

    response = make_response()

    try:
        body = request.get_json()

        nota = Nota(
            not_avaliacao = body.get('not_avaliacao'),
            nor_criterio = body.get('not_criterio'),
            not_valor = body.get('not_valor')
        )

        db.session.add(nota)
        db.session.commit()

        response.status_code = 201

        return jsonify({"content":nota.as_dict()})

    except Exception as e:
        response.status_code = 500
        raise e

@app.get('/avaliacao/nota/')
def note_per_evaluated() :

    id_evalueted = request.args.get('avaliado')
    id_project = request.args.get('projeto')

    avaliacao = select(Avaliacao).where(Avaliacao.ava_avaliado == id_evalueted,
                                        Avaliacao.ava_projeto == id_project)
    
    avaliacoes = db.session.execute(avaliacao)

    ids_avaliacoes = [row[0].ava_id for row in avaliacoes]
    nota = select(Nota).where(Nota.not_avaliacao.in_(ids_avaliacoes))

    notas = db.session.execute(nota)
    notas_json = [row[0].as_dict() for row in notas]

    
    return jsonify(notas_json)

@app.get('/avaliacao/nota/grupo/')
def note_per_team():
    
    id_equipe = request.args.get('equipe')

    equipe_stmt = select(Equipe).where(Equipe.equ_id == id_equipe)
    equipe = db.session.execute(equipe_stmt)

    for row in equipe:
        equipe = row[0]
        break

    alunos_na_equipe_stmt = select(Aluno_equipe).where(Aluno_equipe.ale_equipe == equipe.equ_id)
    alunos_na_equipe = db.session.execute(alunos_na_equipe_stmt)

    alunos_na_equipe_id = [row[0].ale_aluno for row in alunos_na_equipe]

    avaliaoces_stmt = select(Avaliacao).where(Avaliacao.ava_avaliado.in_(alunos_na_equipe_id))
    avaliacoes = db.session.execute(avaliaoces_stmt)

    avaliacoes_id = [row[0].ava_id for row in avaliacoes]

    notas_stmt = select(Nota).where(Nota.not_avaliacao.in_(avaliacoes_id))
    notas = db.session.execute(notas_stmt)

    notas_json = [row[0].as_dict() for row in notas]

    return jsonify(notas_json)    


if __name__ == '__main__':

    app.debug = True
    app.run()
