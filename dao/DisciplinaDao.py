from dao.BaseDao import BaseDao
from models.Disciplina import Disciplina

class DisciplinaDao(BaseDao):

    def __init__(self) -> None:
        super().__init__()

    def convert_entity_to_dict(self,entity: Disciplina) -> dict:
        
        return {
            "dis_id":entity.dis_id,
            "dis_nome":entity.dis_nome,
            "dis_curso":entity.dis_curso, 
            "dis_periodo":entity.dis_periodo,
            "dis_professor":entity.dis_professor
        }

    def create_disciplina(self,json: dict) -> Disciplina:

        return Disciplina(
            dis_nome = json["dis_nome"],
            dis_curso = json["dis_curso"],
            dis_periodo = json["dis_periodo"],
            dis_professor = json["dis_professor"]

        )

    def save_disciplina(self,object):

        entitys = self.create_disciplina(object)

        return self.save_entity_with_commit(entitys)

    def get_all_disciplinas(self) -> list:

        disciplinas = self.session.query(Disciplina).all()

        disciplinas = [self.convert_entity_to_dict(disciplina) for disciplina in disciplinas]

        return disciplinas
    
    def get_disciplina_by_id(self, id_disciplina: int) -> Disciplina:

        disciplina = self.session.query(Disciplina).get(id_disciplina)

        return disciplina
    
    def update_disciplina(self,disciplina_to_be_updated: int, disciplina_info_json: dict) -> None:

        disciplina = self.create_disciplina(disciplina_info_json)
        disciplina.dis_id = disciplina_to_be_updated

        self.update_entity_with_commit(disciplina)
    
    def delete_disciplina(self,disciplina_to_be_deleted: int) -> None:
        
        disciplina = self.get_disciplina_by_id(disciplina_to_be_deleted)

        return self.delete_entity_with_commit(disciplina)