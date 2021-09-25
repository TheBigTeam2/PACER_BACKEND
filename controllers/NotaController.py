from flask.blueprints import Blueprint
from dao.NotaDao import NotaDao
from flask import request, jsonify, make_response

nota_dao = NotaDao()
nota = Blueprint("nota",__name__)

nota.post('/nota')
def insert():

    notas = request.get_json()

    try:
        insertion_result = nota_dao.save_notas_in_mass(notas)

        if insertion_result:

            response =  make_response(jsonify({"inserted_content":notas}),201)
            return response

    except Exception as error:
        response =  make_response(jsonify({"error":error}),500)
        return response