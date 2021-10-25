from dao.BaseDao import BaseDao
from models.Equipe import Equipe

class EquipeDao(BaseDao):

    def __init__(self) -> None:
        super().__init__()

    def convert_entity_to_dict(self,entity: Equipe) -> dict:
        
        return {
            "equ_id":entity.equ_id,
            "equ_nome":entity.equ_nome,
            "equ_disciplina":entity.equ_disciplina
        }


    def create_equipe(self,json: dict) -> Equipe:

        return Equipe(
            equ_nome = json["nome"],
            equ_disciplina = json["disciplina"]
        )


    def save_equipe(self,object):

        entitys = self.create_equipe(object)

        return self.save_entity_with_commit(entitys)


    def get_all_equipes(self) -> list:

        equipes = self.session.query(Equipe).all()

        equipes = [self.convert_entity_to_dict(equipe) for equipe in equipes]

        return equipes


    def get_all_equipes_by_disciplina(self,id_disciplina: int) -> list:

        equipes = self.session.query(Equipe).filter(Equipe.equ_disciplina == id_disciplina).all()

        equipes = [self.convert_entity_to_dict(equipe) for equipe in equipes]

        return equipes        