# Modules
import mariadb
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://<username>:<password>@127.0.0.1:3306/PACER"

db = SQLAlchemy(app)

class Nota(db.Model):
    not_id = db.Column(db.Integer, primary_key=True)
    not_avaliacao = db.Column(db.BigInteger)
    not_criterio = db.Column(db.String(32), nullable=False)
    not_valor = db.Column(db.BigInteger, nullable=False)

@app.route('/nota', methods=['POST', 'GET'])
def inserir_notas():
    
    # POST de dados ao banco:
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
    
    # GET dos dados pro banco:
    


def avaliacao():
    pacer = []
    p = '0'
    while p >= '0' and p <= '4':
        print("\nQual valor você dá a Proatividade?")
        p = input("Sua escolha: ")
        pacer.append(p)
        print("\nQual valor você dá a Autonomia?")
        p = input("Sua escolha: ")
        pacer.append(p)
        print("\nQual valor você dá a Colaboracao?")
        p = input("Sua escolha: ")
        pacer.append(p)
        print("\nQual valor você dá a Entrega de Resultado?")
        p = input("Sua escolha: ")
        pacer.append(p)

        print("\nConfirma Seleção? s/n")
        p = input("Sua escolha: ")
        if p == 's':
            return pacer
        else:
            return []


def menu():
    i = 0
    auto = []
    colega = []
    while i != '0' and i != '3':

        # MENU
        print("\nEscolha uma opção:\n1. Realizar a Auto-avaliação\n2. Realizar a Avaliação do Colega\n3. Confirmar Seleções\n0. Sair")
        i = input("Sua escolha: ")
        if i == '0':
            return
        elif i == '1':
            print("\nAuto-Avaliação:")
            auto = avaliacao()
        elif i == '2':
            print("\nAvaliação do Colega:")
            colega = avaliacao()
    return auto, colega

if __name__ == '__main__':

    app.debug = True
    app.run()
