from dao.BaseDao import BaseDao
from models.relationship_tables.aluno_equipe import aluno_equipe

class AlunoEquipeDao(BaseDao):

    def __init__(self) -> None:
        super().__init__()


    def convert_entity_to_dict(self,entity: aluno_equipe) -> dict:
        return {
            "ale_aluno":entity.ale_aluno,
            "ale_equipe":entity.ale_equipe,
        }


    def create_aluno_equipe(self,json: dict) -> aluno_equipe:
        return aluno_equipe(
            ale_aluno = json["alunos"],
            ale_equipe = json["equipe"]
        )


    def save_aluno_equipe(self, equipe, aluno):
        # entitys = self.create_aluno_equipe(object)
        entitys = aluno_equipe(equipe, aluno)
        return self.save_entity_with_commit(entitys)


    def save_alunos_equipe_in_mass(self, object) -> bool:
        entitys = self.create_aluno_equipe(object)
        alunos_collection = entitys.ale_aluno
        equipe = entitys.ale_equipe
        entitys = [self.save_aluno_equipe(equipe, aluno) for aluno in alunos_collection]
        return self.save_entity_in_mass(entitys)


    def get_all_avaliacoes_by_avaliador(self,id_avaliador: int) -> list:
        avaliacoes = self.session.query(aluno_equipe).filter(aluno_equipe.ava_avaliador == id_avaliador).all()
        avaliacoes = [self.convert_entity_to_dict(avaliacao) for avaliacao in avaliacoes]
        return avaliacoes