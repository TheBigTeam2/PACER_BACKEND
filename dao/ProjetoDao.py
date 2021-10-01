from dao.BaseDao import BaseDao
from models.Projeto import Projeto

class ProjetoDao(BaseDao):

    def __init__(self) -> None:
        super().__init__()

    
    def get_projeto_by_id(self,id_projeto: int) -> Projeto:

        projeto = self.session.query(Projeto).filter(Projeto.pro_id == id_projeto).all()[0]

        return projeto