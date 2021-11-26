from flask.blueprints import Blueprint
from dao.EquipeDao import EquipeDao
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

equipe = Blueprint("equipe",__name__)

@equipe.get('/equipes')
@token_required
def get_equipes():
    equipe_dao = EquipeDao()

    return jsonify(equipe_dao.get_all_equipes())


@equipe.get('/equipe')
def get_equipes_by_disciplina_or_projeto():
    equipe_dao = EquipeDao()
    if request.args.get('disciplina'):
        id_avaliador = request.args['disciplina']

        #Logger MongoDB
        tokensplit = request.headers['token'].split('.')[1]
        usu_decoded = json.loads(base64.b64decode(tokensplit + '=' * (-len(tokensplit) % 4)).decode('utf-8'))['user']['usu_id']
        load_dotenv()
        logevent = 'EquipesGetDisciplinas'
        logger = logging.getLogger(logevent)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(MongoHandler(host=os.getenv("MONGO_URI"), database_name='PacerLogs', collection='Logs'))
        message = "O usuario {} buscou todas as Equipes que participam da Disciplina: {}".format(usu_decoded, id_avaliador)
        hashedmessage = hashlib.sha256((message + usu_decoded + logevent + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + os.getenv('SECRET')).encode('utf-8')).hexdigest() 
        logger.info(message, extra={'usuario': usu_decoded,'hash': hashedmessage})

        return jsonify(equipe_dao.get_all_equipes_by_disciplina(id_avaliador))    

    elif request.args.get('projeto'):
        id_projeto = int(request.args['projeto'])

        #Logger MongoDB
        tokensplit = request.headers['token'].split('.')[1]
        usu_decoded = json.loads(base64.b64decode(tokensplit + '=' * (-len(tokensplit) % 4)).decode('utf-8'))['user']['usu_id']
        load_dotenv()
        logevent = 'EquipesGetDisciplinas'
        logger = logging.getLogger(logevent)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(MongoHandler(host=os.getenv("MONGO_URI"), database_name='PacerLogs', collection='Logs'))
        message = "O usuario {} buscou todas as Equipes que participam do Projeto: {}".format(usu_decoded, id_projeto)
        hashedmessage = hashlib.sha256((message + usu_decoded + logevent + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + os.getenv('SECRET')).encode('utf-8')).hexdigest() 
        logger.info(message, extra={'usuario': usu_decoded,'hash': hashedmessage})

        return jsonify(equipe_dao.get_all_equipes_by_projeto(id_projeto))

@equipe.post('/equipe')
def insert():
    equipe_dao = EquipeDao()
    equipe = request.get_json()

    try:
        insertion_result = equipe_dao.save_equipe(equipe)

        if insertion_result:

            #Logger MongoDB
            tokensplit = request.headers['token'].split('.')[1]
            usu_decoded = json.loads(base64.b64decode(tokensplit + '=' * (-len(tokensplit) % 4)).decode('utf-8'))['user']['usu_id']
            load_dotenv()
            logevent = 'EquipePost'
            logger = logging.getLogger(logevent)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(MongoHandler(host=os.getenv("MONGO_URI"), database_name='PacerLogs', collection='Logs'))
            message = "O usuario {} criou uma nova Equipe: {}".format(usu_decoded, equipe['equ_nome'])
            hashedmessage = hashlib.sha256((message + usu_decoded + logevent + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + os.getenv('SECRET')).encode('utf-8')).hexdigest() 
            logger.info(message, extra={'usuario': usu_decoded,'hash': hashedmessage})

            response =  make_response(jsonify({"inserted_content":equipe}),201)
            return response

    except Exception as error:
        response = make_response(jsonify({"error":"Esse professor nao existe"}),500)
        return response

@equipe.put('/equipe')
def update():
    equipe_dao = EquipeDao()
    if request.args['id']:
        id_equipe = request.args['id']
        equipe_json = request.get_json()
        equipe = equipe_dao.get_equipe_by_id(id_equipe)

        if equipe:

            #Logger MongoDB
            old_equipe = equipe_dao.convert_entity_to_dict(equipe)
            equipes_diff = diff(old_equipe, equipe_json)
            print(old_equipe)
            print(equipe_json)
            print(equipes_diff)
            if equipes_diff:
                tokensplit = request.headers['token'].split('.')[1]
                usu_decoded = json.loads(base64.b64decode(tokensplit + '=' * (-len(tokensplit) % 4)).decode('utf-8'))['user']['usu_id']
                load_dotenv()
                logevent = 'EquipePut'
                logger = logging.getLogger(logevent)
                logger.setLevel(logging.DEBUG)
                logger.addHandler(MongoHandler(host=os.getenv("MONGO_URI"), database_name='PacerLogs', collection='Logs'))
                message = "O usuario {} modificou os seguintes campos da Equipe {}:".format(usu_decoded, old_equipe['equ_nome'])
                if equipes_diff:
                    for key in equipes_diff.keys(): 
                        if isinstance(key, str) and isinstance(old_equipe[key], list):
                            for i in range(0, len(old_equipe[key])):
                                subequipes_diff = diff(old_equipe[key][i], equipe_json[key][i])
                                for subkey in subequipes_diff.keys():
                                    if isinstance(subkey, str):
                                        troca = ' Campo: ' + subkey + ' Em: ' + str(key) + ' De: ' + str(old_equipe[key][i][subkey]) + ' Para: ' + str(equipe_json[key][i][subkey])
                                        message += troca
                        else:
                            if isinstance(key, str):
                                troca = ' Campo: ' + key + ' De: ' + str(old_equipe[key]) + ' Para: ' + str(equipe_json[key])
                                message += troca
                hashedmessage = hashlib.sha256((message + usu_decoded + logevent + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + os.getenv('SECRET')).encode('utf-8')).hexdigest() 
                logger.info(message, extra={'usuario': usu_decoded,'hash': hashedmessage})

            equipe_dao.update_equipe(id_equipe,equipe_json)
            response = make_response(jsonify({"updated_register":id_equipe}),200)

        else:
            response = make_response(jsonify({"error":"register not found"}),500)
   
    else:
        response = make_response(jsonify({"error":"id argument empty"}),500)

    return response

@equipe.delete('/equipe')
def delete():
    equipe_dao = EquipeDao()
    if request.args['id']:
        id_equipe = request.args['id']
        equipe = equipe_dao.get_equipe_by_id(id_equipe)

        if equipe:
            equipe_dao.delete_equipe(equipe)

            #Logger MongoDB
            tokensplit = request.headers['token'].split('.')[1]
            usu_decoded = json.loads(base64.b64decode(tokensplit + '=' * (-len(tokensplit) % 4)).decode('utf-8'))['user']['usu_id']
            load_dotenv()
            logevent = 'EquipeDelete'
            logger = logging.getLogger(logevent)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(MongoHandler(host=os.getenv("MONGO_URI"), database_name='PacerLogs', collection='Logs'))
            message = "O usuario {} deletou uma Equipe: {}".format(usu_decoded, equipe_dao.convert_entity_to_dict(equipe)['equ_nome'])
            hashedmessage = hashlib.sha256((message + usu_decoded + logevent + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + os.getenv('SECRET')).encode('utf-8')).hexdigest() 
            logger.info(message, extra={'usuario': usu_decoded,'hash': hashedmessage})
            response = make_response(jsonify({"deleted_register":id_equipe}),200)

        else:
            response = make_response(jsonify({"error":"register not found"}),500)
   
    else:
        response = make_response(jsonify({"error":"id argument empty"}),500)

    return response


@equipe.put('/atribuir')
def atribuir():
    equipe_dao = EquipeDao()
    equipe_json = request.get_json()
    id_equipe = equipe_json["equipe"]
    equipe = equipe_dao.get_equipe_by_id(id_equipe)
    if equipe:
        equipe_dao.update_equipe_alunos(id_equipe,equipe_json)
        response = make_response(jsonify({"updated_register":id_equipe}),200)
    else:
        response = make_response(jsonify({"error":"register not found"}),500)
    return response


@equipe.get('/equipe_aluno')
def equipe_by_aluno():
    equipe_dao = EquipeDao()
    if request.args['aluno']:
        aluno = request.args['aluno']

        #Logger MongoDB
        tokensplit = request.headers['token'].split('.')[1]
        usu_decoded = json.loads(base64.b64decode(tokensplit + '=' * (-len(tokensplit) % 4)).decode('utf-8'))['user']['usu_id']
        load_dotenv()
        logevent = 'EquipesGetAlunos'
        logger = logging.getLogger(logevent)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(MongoHandler(host=os.getenv("MONGO_URI"), database_name='PacerLogs', collection='Logs'))
        message = "O usuario {} buscou todas as Equipes que possuem o Aluno: {}".format(usu_decoded, aluno)
        hashedmessage = hashlib.sha256((message + usu_decoded + logevent + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + os.getenv('SECRET')).encode('utf-8')).hexdigest() 
        logger.info(message, extra={'usuario': usu_decoded,'hash': hashedmessage})

        return jsonify(equipe_dao.get_equipes_by_aluno(aluno))