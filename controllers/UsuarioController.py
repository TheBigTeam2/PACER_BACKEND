from flask.blueprints import Blueprint
from dao.UsuarioDao import UsuarioDao
from flask import request, jsonify, make_response

usuario_dao = UsuarioDao()
usuario = Blueprint("usuario",__name__)

@usuario.get('/alunos')
def get_alunos():

    return jsonify(usuario_dao.get_all_usuarios_by_aluno())

@usuario.post('/usuario')
def insert():

    usuario = request.get_json()

    try:
        insertion_result = usuario_dao.save_usuario(usuario)

        if insertion_result:

            response =  make_response(jsonify({"inserted_content":usuario}),201)
            return response

    except Exception as error:
        raise error