from werkzeug.wrappers import response
from services.Auth import AuthService
from flask import Blueprint, request, make_response, jsonify

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

            return make_response(jsonify({"authenticated":True,"authentication":token}),200)

        return make_response(jsonify({"authenticated":False,"error":"Invalid user or password"}),500)

    return make_response(jsonify({"authenticated":False,"error":"Provide a token or an user/password"}),500)