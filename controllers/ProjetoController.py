from flask.blueprints import Blueprint
from sqlalchemy.sql.expression import null
from dao.ProjetoDao import ProjetoDao 
from flask import request, jsonify, make_response
from services.Auth import AuthService, token_required
from dao.DisciplinaDao import DisciplinaDao
from dao.EquipeDao import EquipeDao

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

projeto = Blueprint("projeto",__name__)

@projeto.get('/projetos')
@token_required
def get_projetos():
    projeto_dao = ProjetoDao()

    '''
    #Logger MongoDB
    tokensplit = request.headers['token'].split('.')[1]
    usu_decoded = json.loads(base64.b64decode(tokensplit + '=' * (-len(tokensplit) % 4)).decode('utf-8'))['user']['usu_id']
    load_dotenv()
    logevent = 'ProjetoGet'
    logger = logging.getLogger(logevent)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(MongoHandler(host=os.getenv("MONGO_URI"), database_name='PacerLogs', collection='Logs'))
    message = "O usuario {} buscou todos os Projetos".format(usu_decoded)
    hashedmessage = hashlib.sha256((message + usu_decoded + logevent + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + os.getenv('SECRET')).encode('utf-8')).hexdigest() 
    logger.info(message, extra={'usuario': usu_decoded,'hash': hashedmessage})
    '''

    return jsonify(projeto_dao.get_all_projetos())

@projeto.post('/projeto')
@token_required
def insert():
    projeto_dao = ProjetoDao()
    projeto = request.get_json()

    #Logger Setup
    tokensplit = request.headers['token'].split('.')[1]
    usu_decoded = json.loads(base64.b64decode(tokensplit + '=' * (-len(tokensplit) % 4)).decode('utf-8'))['user']['usu_id']
    load_dotenv()

    try:
        insertion_result = projeto_dao.save_projeto(projeto)

        if insertion_result:

            #Logger MongoDB
            logevent = 'ProjetoPost'
            logger = logging.getLogger(logevent)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(MongoHandler(host=os.getenv("MONGO_URI"), database_name='PacerLogs', collection='Logs'))
            message = "O usuario {} criou um novo Projeto: {}".format(usu_decoded, projeto['pro_tema'])
            hashedmessage = hashlib.sha256((message + usu_decoded + logevent + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + os.getenv('SECRET')).encode('utf-8')).hexdigest() 
            logger.info(message, extra={'usuario': usu_decoded,'hash': hashedmessage})

            response =  make_response(jsonify({"inserted_content":projeto}),201)
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
    
@projeto.put('/projeto')
@token_required
def update():
    projeto_dao = ProjetoDao()
    if request.args['id']:
        id_projeto = request.args['id']
        projeto_json = request.get_json()
        projeto = projeto_dao.get_projeto_by_id(id_projeto)

        if projeto:
            
            #Logger MongoDB
            old_projeto = projeto_dao.convert_entity_to_dict(projeto)
            projetos_diff = diff(old_projeto, projeto_json)
            if projetos_diff:
                tokensplit = request.headers['token'].split('.')[1]
                usu_decoded = json.loads(base64.b64decode(tokensplit + '=' * (-len(tokensplit) % 4)).decode('utf-8'))['user']['usu_id']
                load_dotenv()
                logevent = 'ProjetoPut'
                logger = logging.getLogger(logevent)
                logger.setLevel(logging.DEBUG)
                logger.addHandler(MongoHandler(host=os.getenv("MONGO_URI"), database_name='PacerLogs', collection='Logs'))
                message = "O usuario {} modificou os seguintes campos do Projeto {}:".format(usu_decoded, old_projeto['pro_tema'])
                if projetos_diff:
                    for key in projetos_diff.keys(): 
                        if isinstance(key, str) and isinstance(old_projeto[key], list):
                            for i in range(0, len(old_projeto[key])):
                                subprojetos_diff = diff(old_projeto[key][i], projeto_json[key][i])
                                for subkey in subprojetos_diff.keys():
                                    if isinstance(subkey, str):
                                        troca = ' Campo: ' + subkey + ' Em: ' + str(key) + ' De: ' + str(old_projeto[key][i][subkey]) + ' Para: ' + str(projeto_json[key][i][subkey])
                                        message += troca
                        else:
                            if isinstance(key, str):
                                troca = ' Campo: ' + key + ' De: ' + str(old_projeto[key]) + ' Para: ' + str(projeto_json[key])
                                message += troca
                hashedmessage = hashlib.sha256((message + usu_decoded + logevent + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + os.getenv('SECRET')).encode('utf-8')).hexdigest() 
                logger.info(message, extra={'usuario': usu_decoded,'hash': hashedmessage})

            projeto_dao.update_projeto(id_projeto,projeto_json)
            response = make_response(jsonify({"updated_register":id_projeto}),200)

        else:
            response = make_response(jsonify({"error":"register not found"}),500)
   
    else:
        response = make_response(jsonify({"error":"id argument empty"}),500)

    return response

@projeto.delete('/projeto')
@token_required
def delete():
    projeto_dao = ProjetoDao()

    if request.args['id']:
        id_projeto = request.args['id']
        projeto_json = request.get_json()
        projeto = projeto_dao.get_projeto_by_id(id_projeto)

        if projeto:
            resp = projeto_dao.delete_projeto(id_projeto)
            if (resp):

                #Logger MongoDB
                tokensplit = request.headers['token'].split('.')[1]
                usu_decoded = json.loads(base64.b64decode(tokensplit + '=' * (-len(tokensplit) % 4)).decode('utf-8'))['user']['usu_id']
                load_dotenv()
                logevent = 'ProjetoDelete'
                logger = logging.getLogger(logevent)
                logger.setLevel(logging.DEBUG)
                logger.addHandler(MongoHandler(host=os.getenv("MONGO_URI"), database_name='PacerLogs', collection='Logs'))
                message = "O usuario {} deletou um Projeto: {}".format(usu_decoded, projeto_dao.convert_entity_to_dict(projeto)['pro_tema'])
                hashedmessage = hashlib.sha256((message + usu_decoded + logevent + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + os.getenv('SECRET')).encode('utf-8')).hexdigest() 
                logger.info(message, extra={'usuario': usu_decoded,'hash': hashedmessage})

                response = make_response(jsonify({"deleted_register":id_projeto}),200)

            else:
                response = make_response(jsonify({"error":resp}),500)
   
        else:
            response = make_response(jsonify({"error":"id argument empty"}),500)

    return response


## RELACIONANDO PROJETOS E EQUIPES

@projeto.get('/projeto_equipe')
@token_required
def buscar_projetos_da_equipe():
    projeto_dao = ProjetoDao()
    equipe = request.args['equipe']

    return jsonify(projeto_dao.buscar_projetos_da_equipe(equipe))


@projeto.post('/projeto_equipe')
@token_required
def incluir_projeto_equipe():
    projeto_dao = ProjetoDao()
    json = request.get_json()

    try:
        insertion_result = projeto_dao.incluir_projeto_equipe(json)

        if insertion_result:
            response =  make_response(jsonify({"inserted_content":json}),201)
            return response
        else:
            response = make_response(jsonify({"error":"Entrada duplicada"}),500)
            return response

    except Exception as error:
        print(error)
        response = make_response(jsonify({"error":"Entrada duplicada"}),500)
        return response


@projeto.put('/projeto_equipe')
@token_required
def substituir_projeto_equipe():
    projeto_dao = ProjetoDao()
    json = request.get_json()

    try:
        update_result = projeto_dao.substituir_projeto_equipe(json)
        if update_result:
            response = make_response(jsonify({"Updated_content":json}), 200)
            return response
    except Exception as error:
        print(error)
        response = make_response(jsonify({"error":"Bad request"}),400)
        return response


@projeto.delete('/projeto_equipe')
@token_required
def remover_projeto_equipe():
    projeto_dao = ProjetoDao()
    json = {
        "projeto": request.args["projeto"],
        "equipe": request.args["equipe"]
    }

    deletion_result = projeto_dao.remover_projeto_equipe(json)
    if deletion_result:
        if deletion_result == 404:
            response = make_response("Content_not_found: equipe/projeto não relacionados", 404)
        else:
            response = make_response(jsonify({"Removed_content":json}), 200)
        return response

@projeto.get('/buscar_sprints_do_projeto')
@token_required
def buscar_sprints_do_projeto():
    projeto_dao = ProjetoDao()
    if request.args.get('projeto'):
        sprints = projeto_dao.buscar_sprints_do_projeto(request.args.get('projeto'))
        return make_response(jsonify(sprints), 200)
    else:
        return make_response(jsonify({'mensagem': 'É necessário passar o projeto!'}), 422) 