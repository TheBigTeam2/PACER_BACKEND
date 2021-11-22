from dao.BaseDao import BaseDao
from dao.NotaDao import NotaDao
from models.Avaliacao import Avaliacao
from dao.ProjetoDao import ProjetoDao
import random

class AvaliacaoDao(BaseDao):

    def convert_entity_to_dict(self,entity: Avaliacao) -> dict:
        nota_dao = NotaDao()
        return {
            "ava_id":entity.ava_id,
            "ava_sprint":entity.ava_sprint,
            "ava_inicio":entity.ava_inicio,
            "ava_termino":entity.ava_termino,
            "ava_avaliado":entity.ava_avaliado,
            "ava_avaliador":entity.ava_avaliador,
            "ava_projeto":entity.ava_projeto,
            "ava_notas":[nota_dao.convert_entity_to_dict(nota) for nota in entity.notas]
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

    def sort_avaliacoes(self, avaliacoes: list) -> dict:

        projeto_dao = ProjetoDao()

        for avaliacao in avaliacoes:
            projeto = projeto_dao.get_projeto_by_id(avaliacao.get('ava_projeto'))
            self._handle_equipes_in_projeto(projeto.equipes, avaliacao)

    def _handle_equipes_in_projeto(self, equipes: list, avaliacao: dict):

        avaliacoes_to_be_done = list()

        for equipe in equipes:
            alunos_in_equipe = equipe.alunos
            random.shuffle(equipe.alunos)
            print(alunos_in_equipe)
            for index in range(len(alunos_in_equipe)):
                self_avaliation = self.create_avaliacao({
                    "ava_sprint":avaliacao.get('ava_sprint'),
                    "ava_inicio":avaliacao.get('ava_inicio'),
                    "ava_termino":avaliacao.get('ava_termino'),
                    "ava_avaliado":alunos_in_equipe[index].usu_id,
                    "ava_avaliador":alunos_in_equipe[index].usu_id,
                    "ava_projeto":avaliacao.get('ava_projeto')
                })

                avaliacoes_to_be_done.append(self_avaliation)
                
                avaliacoes_to_write = self._handle_sort_avaliacoes(alunos_in_equipe, index, avaliacao)
                avaliacoes_to_be_done = avaliacoes_to_be_done + avaliacoes_to_write
        self.save_entity_in_mass(avaliacoes_to_be_done)
        
    def _handle_sort_avaliacoes(self, alunos: list, index: int, avaliacao: dict):

        if len(alunos) == 2:

            avaliador = 0 if index == 1 else 1
            return [self.create_avaliacao({
                    "ava_sprint":avaliacao.get('ava_sprint'),
                    "ava_inicio":avaliacao.get('ava_inicio'),
                    "ava_termino":avaliacao.get('ava_termino'),
                    "ava_avaliado":alunos[index].usu_id,
                    "ava_avaliador":alunos[avaliador].usu_id,
                    "ava_projeto":avaliacao.get('ava_projeto')
                })]
        
        else:
            
            first_to_be_avaliado = index + 1
            second_to_be_avaliado = index + 2

            if first_to_be_avaliado > len(alunos) -1:
                first_to_be_avaliado = 0

            if second_to_be_avaliado > len(alunos) -1:
                second_to_be_avaliado = 1

                if second_to_be_avaliado == index:
                    second_to_be_avaliado = second_to_be_avaliado - 1
            
            first = self.create_avaliacao({
                    "ava_sprint":avaliacao.get('ava_sprint'),
                    "ava_inicio":avaliacao.get('ava_inicio'),
                    "ava_termino":avaliacao.get('ava_termino'),
                    "ava_avaliado":alunos[index].usu_id,
                    "ava_avaliador":alunos[first_to_be_avaliado].usu_id,
                    "ava_projeto":avaliacao.get('ava_projeto')
                })

            second = self.create_avaliacao({
                    "ava_sprint":avaliacao.get('ava_sprint'),
                    "ava_inicio":avaliacao.get('ava_inicio'),
                    "ava_termino":avaliacao.get('ava_termino'),
                    "ava_avaliado":alunos[index].usu_id,
                    "ava_avaliador":alunos[second_to_be_avaliado].usu_id,
                    "ava_projeto":avaliacao.get('ava_projeto')
                })

            return [first, second]



