from flask.blueprints import Blueprint
from dao.CriterioDao import CriterioDao
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


criterio = Blueprint("criterio",__name__)

@criterio.get('/criterios')
@token_required
def get_criterios():
    criterio_dao = CriterioDao()
    return jsonify(criterio_dao.get_all_criterios())

@criterio.post('/criterio')
def insert():
    criterio_dao = CriterioDao()
    criterio = request.get_json()

    try:
        insertion_result = criterio_dao.save_criterio(criterio)

        if insertion_result:

            #Logger MongoDB
            tokensplit = request.headers['token'].split('.')[1]
            usu_decoded = json.loads(base64.b64decode(tokensplit + '=' * (-len(tokensplit) % 4)).decode('utf-8'))['user']['usu_nome']
            load_dotenv()
            logevent = 'CriterioPost'
            logger = logging.getLogger(logevent)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(MongoHandler(host=os.getenv("MONGO_URI"), database_name='PacerLogs', collection='Logs'))
            message = "O usuario {} criou um novo Critério: {}".format(usu_decoded, criterio['nome'])
            hashedmessage = hashlib.sha256((message + usu_decoded + logevent + str(datetime.datetime.utcnow()) + os.getenv('SECRET')).encode('utf-8')).hexdigest() 
            logger.info(message, extra={'hash': hashedmessage})

            response =  make_response(jsonify({"inserted_content":criterio}),201)
            return response
        else:
            response = make_response(jsonify({"error":"Entrada duplicada"}),500)
            return response

    except Exception as error:
        response = make_response(jsonify({"error":str(error)}),500)
        return response
    
@criterio.put('/criterio')
def update():
    criterio_dao = CriterioDao()
    if request.args['id']:
        id_criterio = request.args['id']
        criterio_json = request.get_json()
        criterio = criterio_dao.get_criterio_by_id(id_criterio)

        if criterio:
            criterio_dao.update_criterio(id_criterio,criterio_json)
            response = make_response(jsonify({"updated_register":id_criterio}),200)

        else:
            response = make_response(jsonify({"error":"register not found"}),500)
   
    else:
        response = make_response(jsonify({"error":"id argument empty"}),500)

    return response

@criterio.delete('/criterio')
def delete():
    criterio_dao = CriterioDao()

    if request.args['id']:
        id_criterio = request.args['id']
        criterio_json = request.get_json()
        criterio = criterio_dao.get_criterio_by_id(id_criterio)

        if criterio:
            resp = criterio_dao.delete_criterio(id_criterio)
            if (resp):
                response = make_response(jsonify({"deleted_register":id_criterio}),200)

            else:
                response = make_response(jsonify({"error":resp}),500)
   
        else:
            response = make_response(jsonify({"error":"id argument empty"}),500)

    return response