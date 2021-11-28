from flask.blueprints import Blueprint
from dao.NotaDao import NotaDao
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

nota = Blueprint("nota",__name__)

@token_required
@nota.post('/nota')
def insert():
    nota_dao = NotaDao()
    notas = request.get_json()

    #Logger Setup
    tokensplit = request.headers['token'].split('.')[1]
    usu_decoded = json.loads(base64.b64decode(tokensplit + '=' * (-len(tokensplit) % 4)).decode('utf-8'))['user']['usu_id']
    load_dotenv()

    try:
        insertion_result = nota_dao.save_notas_in_mass(notas)

        if insertion_result:

            #Logger MongoDB
            logevent = 'NotaPost'
            logger = logging.getLogger(logevent)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(MongoHandler(host=os.getenv("MONGO_URI"), database_name='PacerLogs', collection='Logs'))
            message = "O usuario {} postou notas relacionadas a avaliação: {}".format(usu_decoded, notas[0]['avaliacao'])
            hashedmessage = hashlib.sha256((message + usu_decoded + logevent + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + os.getenv('SECRET')).encode('utf-8')).hexdigest() 
            logger.info(message, extra={'usuario': usu_decoded,'hash': hashedmessage})

            response =  make_response(jsonify({"inserted_content":notas}),201)
            return response
        else:
            response = make_response(jsonify({"error":"Entrada duplicada"}),500)
            return response

    except Exception as error:

        #Logger MongoDB Error 
        logevent = 'ERROR'
        logger = logging.getLogger(logevent)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(MongoHandler(host=os.getenv("MONGO_URI"), database_name='PacerLogs', collection='Logs'))
        message = "O usuario {} gerou um erro: {}".format(usu_decoded, str(error))
        hashedmessage = hashlib.sha256((message + usu_decoded + logevent + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + os.getenv('SECRET')).encode('utf-8')).hexdigest() 
        logger.critical(message, extra={'usuario': usu_decoded,'hash': hashedmessage})

        response = make_response(jsonify({"error":str(error)}),500)
        return response