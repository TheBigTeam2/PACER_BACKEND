from flask.blueprints import Blueprint
from dao.UsuarioDao import UsuarioDao
from flask import request, jsonify, make_response

from models.Usuario import Usuario

usuario_dao = UsuarioDao()
usuario = Blueprint("usuario",__name__)

@usuario.get('/alunos')
def get_alunos():

    return jsonify(usuario_dao.get_all_usuarios_by_aluno())

@usuario.get('/professores')
def get_professores():

    return jsonify(usuario_dao.get_all_usuarios_by_professor())

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

@usuario.put('/usuario')
def update():

    if request.args['id']:

        id_usuario = request.args['id']
        usuario_json = request.get_json()
        usuario = usuario_dao.get_entity_by_id(id_usuario,Usuario)
        if usuario:
            usuario_dao.update_usuario(id_usuario,usuario_json)
            response = make_response(jsonify({"updated_register":id_usuario}),200)

        else:
            response = make_response(jsonify({"error":"register not found"}),500)
   
    else:
        response = make_response(jsonify({"error":"id argument empty"}),500)

    return response

@usuario.delete('/usuario')
def delete():
    if request.args['id']:
        id_usuario = request.args['id']
        usuario = usuario_dao.get_entity_by_id(id_usuario,Usuario)

        if id_usuario:
            usuario_dao.delete_usuario(usuario)
            response = make_response(jsonify({"deleted_register":id_usuario}),200)

        else:
            response = make_response(jsonify({"error":"register not found"}),500)
   
    else:
        response = make_response(jsonify({"error":"id argument empty"}),500)

    return response

            