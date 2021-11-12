from flask.blueprints import Blueprint
from dao.DisciplinaDao import DisciplinaDao 
from flask import request, jsonify, make_response

disciplina = Blueprint("disciplina",__name__)

@disciplina.get('/disciplinas')
def get_disciplinas():
    disciplina_dao = DisciplinaDao()
    return jsonify(disciplina_dao.get_all_disciplinas())

@disciplina.post('/disciplina')
def insert():
    disciplina_dao = DisciplinaDao()
    disciplina = request.get_json()

    try:
        insertion_result = disciplina_dao.save_disciplina(disciplina)

        if insertion_result:
            response =  make_response(jsonify({"inserted_content":disciplina}),201)
            return response
        else:
            response = make_response(jsonify({"error":"Esse professor nao existe"}),500)
            return response

    except Exception as error:
        response = make_response(jsonify({"error":"Esse professor nao existe"}),500)
        return response
    
@disciplina.put('/disciplina')
def update():
    disciplina_dao = DisciplinaDao()
    if request.args['id']:
        id_disciplina = request.args['id']
        disciplina_json = request.get_json()
        disciplina = disciplina_dao.get_disciplina_by_id(id_disciplina)

        if disciplina:
            disciplina_dao.update_disciplina(id_disciplina,disciplina_json)
            response = make_response(jsonify({"updated_register":id_disciplina}),200)

        else:
            response = make_response(jsonify({"error":"register not found"}),500)
   
    else:
        response = make_response(jsonify({"error":"id argument empty"}),500)

    return response

@disciplina.delete('/disciplina')
def delete():
    disciplina_dao = DisciplinaDao()

    if request.args['id']:
        id_disciplina = request.args['id']
        disciplina_json = request.get_json()
        disciplina = disciplina_dao.get_disciplina_by_id(id_disciplina)

        if disciplina:
            resp = disciplina_dao.delete_disciplina(id_disciplina)
            if (resp):
                response = make_response(jsonify({"deleted_register":id_disciplina}),200)

            else:
                response = make_response(jsonify({"error":resp}),500)
   
        else:
            response = make_response(jsonify({"error":"id argument empty"}),500)

    return response