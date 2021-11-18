from flask.blueprints import Blueprint
from sqlalchemy.sql.expression import null
from dao.ProjetoDao import ProjetoDao 
from flask import request, jsonify, make_response
from services.Auth import AuthService, token_required
from dao.DisciplinaDao import DisciplinaDao
from dao.EquipeDao import EquipeDao

projeto = Blueprint("projeto",__name__)

@projeto.get('/projetos')
#@token_required
def get_projetos():
    projeto_dao = ProjetoDao()
    return jsonify(projeto_dao.get_all_projetos())

@projeto.post('/projeto')
def insert():
    projeto_dao = ProjetoDao()
    projeto = request.get_json()

    try:
        insertion_result = projeto_dao.save_projeto(projeto)

        if insertion_result:
            response =  make_response(jsonify({"inserted_content":projeto}),201)
            return response
        else:
            response = make_response(jsonify({"error":"Entrada duplicada"}),500)
            return response

    except Exception as error:
        print(error)
        response = make_response(jsonify({"error":"Entrada duplicada"}),500)
        return response
    
@projeto.put('/projeto')
def update():
    projeto_dao = ProjetoDao()
    if request.args['id']:
        id_projeto = request.args['id']
        projeto_json = request.get_json()
        projeto = projeto_dao.get_projeto_by_id(id_projeto)

        if projeto:
            projeto_dao.update_projeto(id_projeto,projeto_json)
            response = make_response(jsonify({"updated_register":id_projeto}),200)

        else:
            response = make_response(jsonify({"error":"register not found"}),500)
   
    else:
        response = make_response(jsonify({"error":"id argument empty"}),500)

    return response

@projeto.delete('/projeto')
def delete():
    projeto_dao = ProjetoDao()

    if request.args['id']:
        id_projeto = request.args['id']
        projeto_json = request.get_json()
        projeto = projeto_dao.get_projeto_by_id(id_projeto)

        if projeto:
            resp = projeto_dao.delete_projeto(id_projeto)
            if (resp):
                response = make_response(jsonify({"deleted_register":id_projeto}),200)

            else:
                response = make_response(jsonify({"error":resp}),500)
   
        else:
            response = make_response(jsonify({"error":"id argument empty"}),500)

    return response


## RELACIONANDO PROJETOS E EQUIPES

@projeto.post('/projeto_equipe')
def incluir_projeto_equipe():
    projeto_dao = ProjetoDao()
    json = request.get_json()

    try:
        insertion_result = projeto_dao.incluir_projeto_equipe(json)

        if insertion_result:
            response =  make_response(jsonify({"inserted_content":json}),201)
            return response
        else:
            response = make_response(jsonify({"error":"Entrada duplicada"}),500)
            return response

    except Exception as error:
        print(error)
        response = make_response(jsonify({"error":"Entrada duplicada"}),500)
        return response


@projeto.put('/projeto_equipe')
def substituir_projeto_equipe():
    projeto_dao = ProjetoDao()
    json = request.get_json()

    try:
        update_result = projeto_dao.substituir_projeto_equipe(json)
        if update_result:
            response = make_response(jsonify({"Updated_content":json}), 200)
            return response
    except Exception as error:
        print(error)
        response = make_response(jsonify({"error":"Bad request"}),400)
        return response


@projeto.delete('/projeto_equipe')
def remover_projeto_equipe():
    projeto_dao = ProjetoDao()
    json = request.get_json()

    deletion_result = projeto_dao.remover_projeto_equipe(json)
    if deletion_result:
        if deletion_result == 404:
            response = make_response("Content_not_found: equipe/projeto não relacionados", 404)
        else:
            response = make_response(jsonify({"Removed_content":json}), 200)
        return response