from dao.BaseDao import BaseDao
from pymongo import MongoClient
import os
import datetime
import hashlib
from dotenv import load_dotenv

class LogsDao(BaseDao):

    def __init__(self) -> None:
        super().__init__()

    def convert_entity_to_dict(self,log) -> dict:

        id = log['_id']
        timestamp = datetime.datetime.strftime(log['timestamp'], "%Y-%m-%d %H:%M:%S")
        level = log['level']
        thread = log['thread']
        threadName = log['threadName']
        message = log['message']
        loggerName = log['loggerName']
        fileName = log['fileName']
        module = log['module']
        method = log['method']
        lineNumber = log['lineNumber']
        usuario = log['usuario']
        hash = log['hash']

        load_dotenv()
        novahash = hashlib.sha256((message + usuario + loggerName + timestamp + os.getenv('SECRET')).encode('utf-8')).hexdigest()
        verificado = (hash == novahash)
        return {
            'id': str(id),
            'timestamp': timestamp,
            'level': level,
            'thread': thread,
            'threadName': threadName,
            'message': message,
            'fileName': fileName,
            'module': module,
            'method': method,
            'lineNumber': lineNumber,
            'usuario': usuario,
            'hash': hash,
            'verificado': verificado
        }

    def get_all_logs(self) -> list:
        
        client = MongoClient(os.getenv("MONGO_URI"))
        db = client['PacerLogs']
        logs = db['Logs'].find()

        logs = [self.convert_entity_to_dict(log) for log in logs]

        return logs