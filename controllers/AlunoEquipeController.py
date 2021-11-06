from flask.blueprints import Blueprint
from dao.AlunoEquipeDao import AlunoEquipeDao
from flask import request, jsonify, make_response

from models.relationship_tables.aluno_equipe import aluno_equipe

alunoequipe = Blueprint("alunoequipe",__name__)

'''
@usuario.get('/alunos')
def get_alunos():
    usuario_dao = UsuarioDao()
    return jsonify(usuario_dao.get_all_usuarios_by_aluno())

@usuario.get('/professores')
def get_professores():
    usuario_dao = UsuarioDao()
    return jsonify(usuario_dao.get_all_usuarios_by_professor())
'''

@alunoequipe.post('/miajuda')
def insert():

    aluno_equipe = request.get_json()

    try:
        aluno_equipe_dao = AlunoEquipeDao()

        insertion_result = aluno_equipe_dao.save_alunos_equipe_in_mass(aluno_equipe)
        if insertion_result:
            response =  make_response(jsonify({"inserted_content":aluno_equipe}),201)
            return response
        '''
        else:
            response = make_response(jsonify({"error":"register duplicated"}),500)
            return response
        '''
    except Exception as error:
        # response = make_response(jsonify({"error":"Entrada duplicada"}),500)
        raise error

'''
@usuario.put('/usuario')
def update():

    if request.args['id']:

        usuario_dao = UsuarioDao()
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
        usuario_dao = UsuarioDao()
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

'''
            