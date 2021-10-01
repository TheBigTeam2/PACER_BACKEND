from models.Aluno import Aluno
from models.Projeto import Projeto
from models.Equipe import Equipe
from dao.ProjetoDao import ProjetoDao
from dao.AvaliacaoDao import AvaliacaoDao
import random

class AvaliacaoService:

    def __init__(self) -> None:
        self.projeto_dao = ProjetoDao()
        self.avaliacao_dao = AvaliacaoDao()
        self.randons_drafts = []


    def sort_avaliacoes(self,aluno: Aluno,equipe: Equipe,create_avaliacoes_payload: dict) -> int:

        random_avaliação = random.randint(0,len(equipe.alunos)-1)

        if not equipe.alunos[random_avaliação].alu_ra == aluno.alu_ra and random_avaliação not in self.randons_drafts:
                
            common_dict = {
                "ava_sprint":create_avaliacoes_payload.get('sprint'),
                "ava_inicio":create_avaliacoes_payload.get('inicio'),
                "ava_termino":create_avaliacoes_payload.get('termino'),
                "ava_avaliador":aluno.usu_id,
                "ava_projeto":create_avaliacoes_payload.get('projeto')

            }

            avaliacao_dict = {
                "ava_avaliado":equipe.alunos[random_avaliação].usu_id,
            }

            auto_avaliacao_dict = {
                "ava_avaliado":aluno.usu_id,
            }

            avaliacao_dict.update(common_dict)
            auto_avaliacao_dict.update(common_dict)

            avaliacao = self.avaliacao_dao.create_avaliacao(avaliacao_dict)
            self.avaliacao_dao.save_entity_with_commit(avaliacao)  

            auto_avaliacao_dict = self.avaliacao_dao.create_avaliacao(auto_avaliacao_dict)
            self.avaliacao_dao.save_entity_with_commit(auto_avaliacao_dict)  

            self.randons_drafts.append(random_avaliação)


        else:
            self.sort_avaliacoes(aluno,equipe,create_avaliacoes_payload)
                

    def create_avaliacoes(self,create_avaliacoes_payload: dict) -> list:

        projeto = self.projeto_dao.get_projeto_by_id(create_avaliacoes_payload.get('projeto'))
        for equipe in projeto.equipes:
            for aluno in equipe.alunos:
                self.sort_avaliacoes(aluno,equipe,create_avaliacoes_payload)
            self.randons_drafts = []











