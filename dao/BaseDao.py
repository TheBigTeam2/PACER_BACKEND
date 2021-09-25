from abc import ABC,abstractmethod
from utils.SingleSession import SingleSession

class BaseDao(ABC):

    def __init__(self) -> None:
        self.session = SingleSession.get_session()

    def save(self,object):
        
        try:
            self.session.add(object)
            return True
        
        except Exception as error:
            print(error)
            return False
    
