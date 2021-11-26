from flask.blueprints import Blueprint
from dao.UsuarioDao import UsuarioDao
from flask import request, jsonify, make_response
from services.Auth import AuthService, token_required 

from models.Usuario import Usuario

#Mongo Variables
import logging.config
from log4mongo.handlers import MongoHandler
import hashlib
from dotenv import load_dotenv
import os
import base64
import datetime
import json
from jsondiff import diff

usuario = Blueprint("usuario",__name__)

@usuario.get('/alunos')
@token_required
def get_alunos():
    usuario_dao = UsuarioDao()

    #Logger MongoDB
    tokensplit = request.headers['token'].split('.')[1]
    usu_decoded = json.loads(base64.b64decode(tokensplit + '=' * (-len(tokensplit) % 4)).decode('utf-8'))['user']['usu_id']
    load_dotenv()
    logevent = 'UsuarioGetAlunos'
    logger = logging.getLogger(logevent)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(MongoHandler(host=os.getenv("MONGO_URI"), database_name='PacerLogs', collection='Logs'))
    message = "O usuario {} buscou todos os Alunos".format(usu_decoded)
    hashedmessage = hashlib.sha256((message + usu_decoded + logevent + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + os.getenv('SECRET')).encode('utf-8')).hexdigest() 
    logger.info(message, extra={'usuario': usu_decoded,'hash': hashedmessage})

    return jsonify(usuario_dao.get_all_usuarios_by_aluno())

@usuario.get('/professores')
def get_professores():
    usuario_dao = UsuarioDao()

    #Logger MongoDB
    tokensplit = request.headers['token'].split('.')[1]
    usu_decoded = json.loads(base64.b64decode(tokensplit + '=' * (-len(tokensplit) % 4)).decode('utf-8'))['user']['usu_id']
    load_dotenv()
    logevent = 'UsuarioGetProfessores'
    logger = logging.getLogger(logevent)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(MongoHandler(host=os.getenv("MONGO_URI"), database_name='PacerLogs', collection='Logs'))
    message = "O usuario {} buscou todos os Professores".format(usu_decoded)
    hashedmessage = hashlib.sha256((message + usu_decoded + logevent + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + os.getenv('SECRET')).encode('utf-8')).hexdigest() 
    logger.info(message, extra={'usuario': usu_decoded,'hash': hashedmessage})

    return jsonify(usuario_dao.get_all_usuarios_by_professor())

@usuario.post('/usuario')
def insert():

    usuario = request.get_json()

    try:
        usuario_dao = UsuarioDao()
        insertion_result = usuario_dao.save_usuario(usuario)
        if insertion_result:

            #Logger MongoDB
            tokensplit = request.headers['token'].split('.')[1]
            usu_decoded = json.loads(base64.b64decode(tokensplit + '=' * (-len(tokensplit) % 4)).decode('utf-8'))['user']['usu_id']
            load_dotenv()
            logevent = 'UsuarioPost'
            logger = logging.getLogger(logevent)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(MongoHandler(host=os.getenv("MONGO_URI"), database_name='PacerLogs', collection='Logs'))
            message = "O usuario {} criou um novo Usuario".format(usu_decoded)
            hashedmessage = hashlib.sha256((message + usu_decoded + logevent + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + os.getenv('SECRET')).encode('utf-8')).hexdigest() 
            logger.info(message, extra={'usuario': usu_decoded,'hash': hashedmessage})

            response =  make_response(jsonify({"inserted_content":usuario}),201)
            return response
        else:
            response = make_response(jsonify({"error":"register duplicated"}),500)
            return response

    except Exception as error:
        response = make_response(jsonify({"error":str(error)}),500)
        return response

@usuario.post('/usuarios')
def insert_in_mass():
    usuario_dao = UsuarioDao()
    usuarios_csv = request.get_json()
    all_usuarios = usuario_dao.get_all_usuarios()
    usuarios_pruned = []

    try:
        for busca in all_usuarios:
            for usu in usuarios_csv:
                if (usu['usu_rg'] == busca['usu_rg']):
                   usuarios_csv.remove(usu)
        
        insertion_result = usuario_dao.save_usuarios_in_mass(usuarios_csv)

        if insertion_result:

            response =  make_response(jsonify({"inserted_content":usuarios_csv}),201)
            return response

    except Exception as error:
        print(error)
        response = make_response(jsonify({"error":"Usuario duplicado"}),500)
        return response


@usuario.put('/usuario')
def update():

    if request.args['id']:

        usuario_dao = UsuarioDao()
        id_usuario = request.args['id']
        usuario_json = request.get_json()
        usuario = usuario_dao.get_entity_by_id(id_usuario,Usuario)
        if usuario:

            #Logger MongoDB
            old_usuario = usuario_dao.convert_entity_to_dict(usuario)
            usuarios_diff = diff(old_usuario, usuario_json)
            if usuarios_diff:
                tokensplit = request.headers['token'].split('.')[1]
                usu_decoded = json.loads(base64.b64decode(tokensplit + '=' * (-len(tokensplit) % 4)).decode('utf-8'))['user']['usu_id']
                load_dotenv()
                logevent = 'UsuarioPut'
                logger = logging.getLogger(logevent)
                logger.setLevel(logging.DEBUG)
                logger.addHandler(MongoHandler(host=os.getenv("MONGO_URI"), database_name='PacerLogs', collection='Logs'))
                message = "O usuario {} modificou o seguinte Usuario: {}".format(usu_decoded, old_usuario['usu_id'])
                hashedmessage = hashlib.sha256((message + usu_decoded + logevent + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + os.getenv('SECRET')).encode('utf-8')).hexdigest() 
                logger.info(message, extra={'usuario': usu_decoded,'hash': hashedmessage})

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

            #Logger MongoDB
            tokensplit = request.headers['token'].split('.')[1]
            usu_decoded = json.loads(base64.b64decode(tokensplit + '=' * (-len(tokensplit) % 4)).decode('utf-8'))['user']['usu_id']
            load_dotenv()
            logevent = 'UsuarioDelete'
            logger = logging.getLogger(logevent)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(MongoHandler(host=os.getenv("MONGO_URI"), database_name='PacerLogs', collection='Logs'))
            message = "O usuario {} deletou o Usuario: {}".format(usu_decoded, usuario_dao.convert_entity_to_dict(usuario)['usu_id'])
            hashedmessage = hashlib.sha256((message + usu_decoded + logevent + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + os.getenv('SECRET')).encode('utf-8')).hexdigest() 
            logger.info(message, extra={'usuario': usu_decoded,'hash': hashedmessage})

            response = make_response(jsonify({"deleted_register":id_usuario}),200)

        else:
            response = make_response(jsonify({"error":"register not found"}),500)
   
    else:
        response = make_response(jsonify({"error":"id argument empty"}),500)

    return response
