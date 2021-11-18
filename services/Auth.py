from sqlalchemy.sql.elements import and_
from sqlalchemy.sql.expression import false
from dao.UsuarioDao import UsuarioDao
from models.Usuario import Usuario
from datetime import datetime, timedelta
import os
import jwt
from dotenv import load_dotenv
from flask import request, jsonify
from functools import wraps
from controllers.route_controlls import routes_access

def token_required(f):
   @wraps(f)
   def decorator(*args,**kwargs):
       auth = AuthService()

       roles = routes_access.get(request.url.split('/')[-1],[])

       token = None
       if 'token' in request.headers:
           token = request.headers['token']
 
       if not token:
           return jsonify({'message': 'a valid token is missing'})

       is_auth = auth.get_role(token,roles)
       
       if is_auth or not roles:
        return f()

       return  {"error":"Invalid role"} 

   return decorator


class AuthService:

    def __init__(self) -> None:
        load_dotenv('./utils/.env')

    def authenticate(self,payload: dict) -> dict:

        return self._user_authentication(payload.get('user'),payload.get('password'))


    def _user_authentication(self,user: str,password: str) -> dict:

        dao_usuario = UsuarioDao()

        usuario = dao_usuario.session.query(Usuario).filter(and_(Usuario.usu_cpf == user,Usuario.usu_senha == password)).one_or_none()

        if usuario:
            token = self._generate_token(usuario)
            return {"cpf":usuario.usu_cpf, "token":token}

        return False

    def _generate_token(self,usuario: Usuario) -> str:
        
        payload = {
            "user":usuario.as_dict(),
            "role":usuario.usu_auth,
            "exp":datetime.utcnow() + timedelta(minutes=30)
        }

        token = jwt.encode(
            payload,os.getenv('SECRET')
        )

        return token

    def _validade_token(self,token):
        
        decoded_token = jwt.decode(token,os.getenv('SECRET'),algorithms=['HS256'])

        if datetime.timestamp(datetime.now()) < decoded_token.get('exp'):
            return decoded_token
        
        return False

    def get_role(self, token, expected_roles):

        decoded_token = self._validade_token(token)

        if decoded_token:

            if decoded_token.get('role') in expected_roles:
                return True
            
            return False

        else:
            return {"authenticated":false,"error":"Token invalid or expired"}