from dao.BaseDao import BaseDao
from models.Criterio import Criterio

class CriterioDao(BaseDao):

    def __init__(self) -> None:
        super().__init__()

    def convert_entity_to_dict(self,entity: Criterio) -> dict:
        
        return {
            "cri_id":entity.cri_id,
            "cri_nome":entity.cri_nome
        }

    def create_criterio(self,json: dict) -> Criterio:

        return Criterio(
            cri_nome = json["nome"],

        )

    def save_criterio(self,object):

        entitys = self.create_criterio(object)

        return self.save_entity_with_commit(entitys)

    def get_all_criterios(self) -> list:

        criterios = self.session.query(Criterio).all()

        criterios = [self.convert_entity_to_dict(criterio) for criterio in criterios]

        return criterios
    
    def update_criterio(self,criterio_id: int):

        criterio = self.session.query(Criterio).get(criterio_id)

        criterio = self.convert_entity_to_dict(criterio)
        
        return self.update_entity_with_commit(criterio)
    
    def delete_criterio(self,criterio_id: int):

        criterio = self.session.query(Criterio).get(criterio_id)

        criterio = self.convert_entity_to_dict(criterio)
        
        return self.delete_entity_with_commit(criterio)