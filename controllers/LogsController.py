from flask.blueprints import Blueprint
from dao.LogsDao import LogsDao
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

logs = Blueprint("logs",__name__)

@logs.get('/logs')
@token_required
def get_logs():
    logs_dao = LogsDao()


    #Logger MongoDB
    tokensplit = request.headers['token'].split('.')[1]
    usu_decoded = json.loads(base64.b64decode(tokensplit + '=' * (-len(tokensplit) % 4)).decode('utf-8'))['user']['usu_id']
    load_dotenv()
    logevent = 'LogsGet'
    logger = logging.getLogger(logevent)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(MongoHandler(host=os.getenv("MONGO_URI"), database_name='PacerLogs', collection='Logs'))
    message = "O usuario {} buscou todos os Logs!".format(usu_decoded)
    hashedmessage = hashlib.sha256((message + usu_decoded + logevent + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + os.getenv('SECRET')).encode('utf-8')).hexdigest() 
    logger.warning(message, extra={'usuario': usu_decoded,'hash': hashedmessage})

    return jsonify(logs_dao.get_all_logs())