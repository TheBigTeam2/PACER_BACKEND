from flask.blueprints import Blueprint
from dao.ProjetoDao import ProjetoDao 
from flask import request, jsonify, make_response
from services.Auth import AuthService, token_required 

projeto = Blueprint("projeto",__name__)

@projeto.get('/projetos')
@token_required
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