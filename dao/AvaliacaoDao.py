from dao.BaseDao import BaseDao
from models.Avaliacao import Avaliacao

class AvaliacaoDao(BaseDao):

    def convert_entity_to_dict(self,entity: Avaliacao) -> dict:
        
        return {
            "ava_id":entity.ava_id,
            "ava_sprint":entity.ava_sprint,
            "ava_inicio":entity.ava_inicio,
            "ava_termino":entity.ava_termino,
            "ava_avaliado":entity.ava_avaliado,
            "ava_avaliador":entity.ava_avaliador,
            "ava_projeto":entity.ava_projeto
        }

    def create_avaliacao(self,json: dict) -> Avaliacao:

        return Avaliacao(
            ava_sprint = json["ava_sprint"],
            ava_inicio = json["ava_inicio"],
            ava_termino = json["ava_termino"],
            ava_avaliado = json["ava_avaliado"],
            ava_avaliador = json["ava_avaliador"],
            ava_projeto = json["ava_projeto"]
        )

    def save_avaliacao_in_mass(self,avaliacoes_collection: list) -> bool:

        entitys = [self.create_avaliacao(avaliacao) for avaliacao in avaliacoes_collection]
        return self.save_entity_in_mass(entitys)

    def get_all_avaliacoes_by_avaliador(self,id_avaliador: int) -> list:

        avaliacoes = self.session.query(Avaliacao).filter(Avaliacao.ava_avaliador == id_avaliador).all()

        avaliacoes = [self.convert_entity_to_dict(avaliacao) for avaliacao in avaliacoes]

        return avaliacoes