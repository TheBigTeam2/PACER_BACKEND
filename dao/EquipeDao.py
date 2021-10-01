from dao.BaseDao import BaseDao
from models.Equipe import Equipe

class EquipeDao(BaseDao):

    def __init__(self) -> None:
        super().__init__()

    
    def get_equipe_by_id(self,id_equipe: int) -> Equipe:

        equipe = self.session.query(Equipe).filter(Equipe.equ_id == id_equipe).one()

        return equipe