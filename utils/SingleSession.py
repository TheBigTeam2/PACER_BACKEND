from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from dotenv import load_dotenv
import os


class SingleSession:

    @staticmethod
    def get_session() -> Session:

        def create_session():

            load_dotenv()
            
            engine = create_engine(os.getenv("BD_URI"))
            
            return Session(engine)

        SingleSession.session = create_session()
        return SingleSession.session