from dao.BaseDao import BaseDao
from models.Nota import Nota

class NotaDao(BaseDao):

    def __init__(self) -> None:
        super().__init__()

    def convert_entity_to_dict(self, entity: Nota) -> dict:

        return {
            "not_id": entity.not_id,
            "not_avaliacao":entity.not_avaliacao,
            "not_criterio": entity.not_criterio,
            "not_valor": entity.not_valor
        } 

    def create_nota(self,json: dict) -> Nota:

        return Nota(
            not_avaliacao = json["avaliacao"],
            not_criterio = json["criterio"],
            not_valor = json["nota"]
        )

    def save_notas_in_mass(self, notas_collection: list):

        entitys = [self.create_nota(nota) for nota in notas_collection]

        return self.save_entity_in_mass(entitys)
