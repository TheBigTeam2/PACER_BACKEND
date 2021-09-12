# Modules
import mariadb
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys

# MariaDB Connection
try:
    conn = mariadb.connect(
        user="root",
        password="root",
        host="127.0.0.1",
        port=3306,
        database="PACER"
    )
except mariadb.Error as e:
    print(f"Error connecting to platform: {e}")
    sys.exit(1)
cur = conn.cursor()

nota = Flask(__name__)
CORS(app)

@app.route('/<string:id>/nota', methods=['POST', 'GET'])
def inserir_notas(id):
    
    # POST de dados ao banco:
    
    
    # GET dos dados pro banco:
    


def inserir(auto, colega):
    #Inserindo Auto-avaliação
    cur.execute("INSERT INTO NOTA (not_criterio, not_valor) VALUES ('Proatividade', ?);", (auto[0],))
    cur.execute("INSERT INTO NOTA (not_criterio, not_valor) VALUES ('Autonomia', ?);", (auto[1],))
    cur.execute("INSERT INTO NOTA (not_criterio, not_valor) VALUES ('Colaboração', ?);", (auto[2],))
    cur.execute("INSERT INTO NOTA (not_criterio, not_valor) VALUES ('Entrega de Resultado', ?);", (auto[3],))

    #Inserindo Avaliação do Colega
    cur.execute("INSERT INTO NOTA (not_criterio, not_valor) VALUES ('Proatividade', ?);", (colega[0],))
    cur.execute("INSERT INTO NOTA (not_criterio, not_valor) VALUES ('Autonomia', ?);", (colega[1],))
    cur.execute("INSERT INTO NOTA (not_criterio, not_valor) VALUES ('Colaboração', ?);", (colega[2],))
    cur.execute("INSERT INTO NOTA (not_criterio, not_valor) VALUES ('Entrega de Resultado', ?);", (colega[3],))
    return 


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
    auto = []
    colega = []
    auto, colega = menu()
    nota.debug = True
    nota.run()
    if auto and colega:
        inserir(auto, colega)
