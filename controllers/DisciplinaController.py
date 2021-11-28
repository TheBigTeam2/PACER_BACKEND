from flask.blueprints import Blueprint
from dao.DisciplinaDao import DisciplinaDao 
from flask import request, jsonify, make_response
from services.Auth import AuthService, token_required 

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

disciplina = Blueprint("disciplina",__name__)

@disciplina.get('/disciplinas')
@token_required
def get_disciplinas():
    disciplina_dao = DisciplinaDao()

    '''
    #Logger MongoDB
    tokensplit = request.headers['token'].split('.')[1]
    usu_decoded = json.loads(base64.b64decode(tokensplit + '=' * (-len(tokensplit) % 4)).decode('utf-8'))['user']['usu_id']
    load_dotenv()
    logevent = 'DisciplinasGet'
    logger = logging.getLogger(logevent)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(MongoHandler(host=os.getenv("MONGO_URI"), database_name='PacerLogs', collection='Logs'))
    message = "O usuario {} buscou todas as Disciplinas".format(usu_decoded)
    hashedmessage = hashlib.sha256((message + usu_decoded + logevent + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + os.getenv('SECRET')).encode('utf-8')).hexdigest() 
    logger.info(message, extra={'usuario': usu_decoded,'hash': hashedmessage})
    '''

    return jsonify(disciplina_dao.get_all_disciplinas())

@disciplina.post('/disciplina')
def insert():
    disciplina_dao = DisciplinaDao()
    disciplina = request.get_json()

    try:
        insertion_result = disciplina_dao.save_disciplina(disciplina)

        if insertion_result:

            #Logger MongoDB
            tokensplit = request.headers['token'].split('.')[1]
            usu_decoded = json.loads(base64.b64decode(tokensplit + '=' * (-len(tokensplit) % 4)).decode('utf-8'))['user']['usu_id']
            load_dotenv()
            logevent = 'DisciplinaPost'
            logger = logging.getLogger(logevent)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(MongoHandler(host=os.getenv("MONGO_URI"), database_name='PacerLogs', collection='Logs'))
            message = "O usuario {} criou uma nova Disciplina: {}".format(usu_decoded, disciplina['dis_nome'])
            hashedmessage = hashlib.sha256((message + usu_decoded + logevent + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + os.getenv('SECRET')).encode('utf-8')).hexdigest() 
            logger.info(message, extra={'usuario': usu_decoded,'hash': hashedmessage})

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

            #Logger MongoDB
            old_disciplina = disciplina_dao.convert_entity_to_dict(disciplina)
            disciplinas_diff = diff(old_disciplina, disciplina_json)
            if disciplinas_diff:
                tokensplit = request.headers['token'].split('.')[1]
                usu_decoded = json.loads(base64.b64decode(tokensplit + '=' * (-len(tokensplit) % 4)).decode('utf-8'))['user']['usu_id']
                load_dotenv()
                logevent = 'DisciplinaPut'
                logger = logging.getLogger(logevent)
                logger.setLevel(logging.DEBUG)
                logger.addHandler(MongoHandler(host=os.getenv("MONGO_URI"), database_name='PacerLogs', collection='Logs'))
                message = "O usuario {} modificou os seguintes campos de uma Disciplina {}:".format(usu_decoded, old_disciplina['dis_nome'])
                if disciplinas_diff:
                    for key in disciplinas_diff.keys(): 
                        if isinstance(key, str) and isinstance(old_disciplina[key], list):
                            for i in range(0, len(old_disciplina[key])):
                                subdisciplinas_diff = diff(old_disciplina[key][i], disciplina_json[key][i])
                                for subkey in subdisciplinas_diff.keys():
                                    if isinstance(subkey, str):
                                        troca = ' Campo: ' + subkey + ' Em: ' + str(key) + ' De: ' + str(old_disciplina[key][i][subkey]) + ' Para: ' + str(disciplina_json[key][i][subkey])
                                        message += troca
                        else:
                            if isinstance(key, str):
                                troca = ' Campo: ' + key + ' De: ' + str(old_disciplina[key]) + ' Para: ' + str(disciplina_json[key])
                                message += troca
                hashedmessage = hashlib.sha256((message + usu_decoded + logevent + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + os.getenv('SECRET')).encode('utf-8')).hexdigest() 
                logger.info(message, extra={'usuario': usu_decoded,'hash': hashedmessage})
            
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

                #Logger MongoDB
                tokensplit = request.headers['token'].split('.')[1]
                usu_decoded = json.loads(base64.b64decode(tokensplit + '=' * (-len(tokensplit) % 4)).decode('utf-8'))['user']['usu_id']
                load_dotenv()
                logevent = 'DisciplinaDelete'
                logger = logging.getLogger(logevent)
                logger.setLevel(logging.DEBUG)
                logger.addHandler(MongoHandler(host=os.getenv("MONGO_URI"), database_name='PacerLogs', collection='Logs'))
                message = "O usuario {} deletou uma Disciplina: {}".format(usu_decoded, disciplina_dao.convert_entity_to_dict(disciplina)['dis_nome'])
                hashedmessage = hashlib.sha256((message + usu_decoded + logevent + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + os.getenv('SECRET')).encode('utf-8')).hexdigest() 
                logger.info(message, extra={'usuario': usu_decoded,'hash': hashedmessage})

                response = make_response(jsonify({"deleted_register":id_disciplina}),200)

            else:
                response = make_response(jsonify({"error":resp}),500)
   
        else:
            response = make_response(jsonify({"error":"id argument empty"}),500)

    return response