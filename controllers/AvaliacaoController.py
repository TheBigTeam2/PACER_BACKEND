from flask import Blueprint, request, jsonify, make_response
from dao.AvaliacaoDao import AvaliacaoDao
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

avaliacao = Blueprint("avaliacao",__name__)

@avaliacao.get('/avaliacao')
@token_required
def get_avaliacao():
    avaliacao_dao = AvaliacaoDao()
    if request.args['avaliador']:
        id_avaliador = request.args['avaliador']

        '''
        #Logger MongoDB
        tokensplit = request.headers['token'].split('.')[1]
        usu_decoded = json.loads(base64.b64decode(tokensplit + '=' * (-len(tokensplit) % 4)).decode('utf-8'))['user']['usu_id']
        load_dotenv()
        logevent = 'AvaliaçãoGet'
        logger = logging.getLogger(logevent)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(MongoHandler(host=os.getenv("MONGO_URI"), database_name='PacerLogs', collection='Logs'))
        message = "O usuario {} buscou pela Avaliação {}".format(usu_decoded, id_avaliador)
        hashedmessage = hashlib.sha256((message + usu_decoded + logevent + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + os.getenv('SECRET')).encode('utf-8')).hexdigest() 
        logger.info(message, extra={'usuario': usu_decoded,'hash': hashedmessage})
        '''

        return jsonify(avaliacao_dao.get_all_avaliacoes_by_avaliador(id_avaliador))

@avaliacao.post('/avaliacao')
@token_required
def post_avaliacao():
    avaliacao_dao = AvaliacaoDao()
    avaliacao = request.get_json()

    #Logger Setup
    tokensplit = request.headers['token'].split('.')[1]
    usu_decoded = json.loads(base64.b64decode(tokensplit + '=' * (-len(tokensplit) % 4)).decode('utf-8'))['user']['usu_id']
    load_dotenv()

    try:
        avaliacao_dao.sort_avaliacoes([avaliacao])

        #Logger MongoDB
        logevent = 'AvaliaçãoPost'
        logger = logging.getLogger(logevent)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(MongoHandler(host=os.getenv("MONGO_URI"), database_name='PacerLogs', collection='Logs'))
        message = "O usuario {} criou uma nova Avaliação: Início em: {}, Término em: {}".format(usu_decoded, avaliacao['ava_inicio'], avaliacao['ava_termino'])
        hashedmessage = hashlib.sha256((message + usu_decoded + logevent + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + os.getenv('SECRET')).encode('utf-8')).hexdigest() 
        logger.info(message, extra={'usuario': usu_decoded,'hash': hashedmessage})

        response =  make_response(jsonify({"inserted_content":avaliacao}),201)
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

        return make_response(jsonify({"error":str(error)}),500)
    

@avaliacao.post('/avaliacao_prof')    
@token_required
def post_avaliacao_prof():
    avaliacao_dao = AvaliacaoDao()
    json = request.get_json()

    #Logger Setup
    tokensplit = request.headers['token'].split('.')[1]
    usu_decoded = json.loads(base64.b64decode(tokensplit + '=' * (-len(tokensplit) % 4)).decode('utf-8'))['user']['usu_id']
    load_dotenv()

    try:
        avaliacao_dao.save_avaliacao_professor(json)

        #Logger MongoDB
        logevent = 'AvaliaçãoPostProfessor'
        logger = logging.getLogger(logevent)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(MongoHandler(host=os.getenv("MONGO_URI"), database_name='PacerLogs', collection='Logs'))
        message = "O professor {} avaliou o aluno: {}".format(usu_decoded, json['aluno'])
        hashedmessage = hashlib.sha256((message + usu_decoded + logevent + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + os.getenv('SECRET')).encode('utf-8')).hexdigest() 
        logger.info(message, extra={'usuario': usu_decoded,'hash': hashedmessage})

        response =  make_response(jsonify({"inserted_content":json}),201)
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

        return make_response(jsonify({"error":str(error)}),500)    