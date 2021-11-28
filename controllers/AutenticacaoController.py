from werkzeug.wrappers import response
from services.Auth import AuthService
from flask import Blueprint, request, make_response, jsonify

#Mongo Variables
import logging.config
from log4mongo.handlers import MongoHandler
import hashlib
from dotenv import load_dotenv
import os
import base64
import datetime
import json

autenticacao = Blueprint("autenticacao",__name__)

@autenticacao.post('/login')
def login():

    auth = AuthService()
    body = request.get_json()

    if request.headers.get('token'):

        user_properties = auth._validade_token(request.headers.get('token'))

        if user_properties:
            return make_response(jsonify({"authenticated":True}),200)

        return make_response(jsonify({"authenticated":False,"error":"Token invalid or expired"}),500)
            
    elif body.get('user') and body.get('password'):

        token = auth.authenticate(body)

        if token:

            #Logger MongoDB
            usu_decoded = str(token['usu_id'])
            load_dotenv()
            logevent = 'Login'
            logger = logging.getLogger(logevent)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(MongoHandler(host=os.getenv("MONGO_URI"), database_name='PacerLogs', collection='Logs'))
            message = "O usuario {} fez Login".format(usu_decoded)
            hashedmessage = hashlib.sha256((message + usu_decoded + logevent + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + os.getenv('SECRET')).encode('utf-8')).hexdigest() 
            logger.info(message, extra={'usuario': usu_decoded,'hash': hashedmessage})

            return make_response(jsonify({"authenticated":True,"authentication":token}),200)

        return make_response(jsonify({"authenticated":False,"error":"Invalid user or password"}),500)

    return make_response(jsonify({"authenticated":False,"error":"Provide a token or an user/password"}),500)