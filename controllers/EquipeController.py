from flask.blueprints import Blueprint
from dao.EquipeDao import EquipeDao
from flask import request, jsonify, make_response

equipe_dao = EquipeDao()
equipe = Blueprint("equipe",__name__)

@equipe.get('/equipes')
def get_equipes():

    return jsonify(equipe_dao.get_all_equipes())


@equipe.get('/equipes')
def get_equipes_by_disciplina():

    if request.args['disciplina']:
        id_avaliador = request.args['disciplina']
        return jsonify(equipe_dao.get_all_equipes_by_disciplina(id_avaliador))    


@equipe.post('/equipe')
def insert():

    equipe = request.get_json()

    try:
        insertion_result = equipe_dao.save_equipe(equipe)

        if insertion_result:

            response =  make_response(jsonify({"inserted_content":equipe}),201)
            return response

    except Exception as error:
        raise error

@equipe.put('/equipe')
def update():

    if request.args['id']:
        id_equipe = request.args['id']
        equipe_json = request.get_json()
        equipe = equipe_dao.get_equipe_by_id(id_equipe)

        if equipe:
            equipe_dao.update_equipe(id_equipe,equipe_json)
            response = make_response(jsonify({"updated_register":id_equipe}),200)

        else:
            response = make_response(jsonify({"error":"register not found"}),500)
   
    else:
        response = make_response(jsonify({"error":"id argument empty"}),500)

    return response

@equipe.delete('/equipe')
def delete():
    if request.args['id']:
        id_equipe = request.args['id']
        equipe = equipe_dao.get_equipe_by_id(id_equipe)

        if equipe:
            equipe_dao.delete_equipe(equipe)
            response = make_response(jsonify({"deleted_register":id_equipe}),200)

        else:
            response = make_response(jsonify({"error":"register not found"}),500)
   
    else:
        response = make_response(jsonify({"error":"id argument empty"}),500)

    return response
