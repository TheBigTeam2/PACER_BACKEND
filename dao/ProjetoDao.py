from dao.BaseDao import BaseDao
from models.Projeto import Projeto

class ProjetoDao(BaseDao):

    def __init__(self) -> None:
        super().__init__()

    def convert_entity_to_dict(self,entity: Projeto) -> dict:
        
        return {
            "pro_id":entity.pro_id,
            "pro_tema":entity.pro_tema,
            "pro_inicio":entity.pro_inicio,
            "pro_termino":entity.pro_termino
        }

    def create_projeto(self,json: dict) -> Projeto:

        return Projeto(
            pro_tema = json["pro_tema"],
            pro_inicio = json["pro_inicio"],
            pro_termino = json["pro_termino"],

        )

    def save_projeto(self,object):

        entitys = self.create_projeto(object)

        return self.save_entity_with_commit(entitys)

    def get_all_projetos(self) -> list:

        projetos = self.session.query(Projeto).all()

        projetos = [self.convert_entity_to_dict(projeto) for projeto in projetos]

        return projetos
    
    def get_projeto_by_id(self, id_projeto: int) -> Projeto:

        projeto = self.session.query(Projeto).get(id_projeto)

        return projeto
    
    def update_projeto(self,projeto_to_be_updated: int, projeto_info_json: dict) -> None:

        projeto = self.create_projeto(projeto_info_json)
        projeto.pro_id = projeto_to_be_updated

        self.update_entity_with_commit(projeto)
    
    def delete_projeto(self,projeto_to_be_deleted: int) -> None:
        
        projeto = self.get_projeto_by_id(projeto_to_be_deleted)

        return self.delete_entity_with_commit(projeto)