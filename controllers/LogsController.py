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
    return jsonify(logs_dao.get_all_logs())