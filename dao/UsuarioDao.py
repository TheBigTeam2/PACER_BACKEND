from pandas.core.frame import DataFrame
from sqlalchemy.orm import session
from sqlalchemy.sql.elements import and_
from sqlalchemy.sql import func
from dao.AvaliacaoDao import AvaliacaoDao
from dao.BaseDao import BaseDao
from dao.NotaDao import NotaDao
from models.Criterio import Criterio
from models.Usuario import Usuario
from models.Avaliacao import Avaliacao
from models.Nota import Nota
import pandas as pd

class UsuarioDao(BaseDao):

    def __init__(self) -> None:
        super().__init__()


    def get_avaliacoes_by_usuario_and_projeto(self,projeto: int, usuario_id: int):
        avaliacao_dao = AvaliacaoDao()
        avaliacoes = self.session.query(Avaliacao).filter(and_(Avaliacao.ava_projeto == projeto,Avaliacao.ava_avaliador == usuario_id)).all()

        return [avaliacao_dao.convert_entity_to_dict(avaliacao) for avaliacao in avaliacoes]

    def convert_entity_to_dict(self,entity: Usuario,projeto: int = None) -> dict:

        if projeto:
            avaliacoes = self.get_avaliacoes_by_usuario_and_projeto(projeto,entity.usu_id)

            return {
                "usu_id":entity.usu_id,
                "usu_rg":entity.usu_rg,
                "usu_cpf":entity.usu_cpf,
                "usu_nome":entity.usu_nome,
                "usu_auth":entity.usu_auth,
                "avaliacoes":avaliacoes
            }
            
        return {
            "usu_id":entity.usu_id,
            "usu_rg":entity.usu_rg,
            "usu_cpf":entity.usu_cpf,
            "usu_nome":entity.usu_nome,
            "usu_auth":entity.usu_auth
        }

    def create_usuario(self,json: dict) -> Usuario:

        return Usuario(
            usu_rg = json["usu_rg"],
            usu_cpf = json["usu_cpf"],
            usu_nome = json["usu_nome"],
            usu_auth = json["usu_auth"],
            usu_senha = "mudar!@#"
        )

    def save_usuario(self,object):

        entitys = self.create_usuario(object)

        return self.save_entity_with_commit(entitys)
    
    def save_usuarios_in_mass(self, usuarios_collection: list):

        entitys = [self.create_usuario(usuario) for usuario in usuarios_collection]

        return self.save_entity_in_mass(entitys)

    def get_all_usuarios_by_aluno(self) -> list:

        alunos = self.session.query(Usuario).filter(Usuario.usu_auth == "Aluno").all()

        alunos = [self.convert_entity_to_dict(aluno) for aluno in alunos]

        return alunos


    def get_all_alunos(self) -> list:
        alunos = self.session.query(Usuario).filter(Usuario.usu_auth == "Aluno").all()

        return alunos

    
    def get_all_usuarios(self) -> list:

        usuarios = self.session.query(Usuario).all()

        usuarios = [self.convert_entity_to_dict(usuario) for usuario in usuarios]

        return usuarios
    
    def get_all_usuarios_by_professor(self) -> list:

        professores = self.session.query(Usuario).filter(Usuario.usu_auth == "Professor").all()

        professores = [self.convert_entity_to_dict(professor) for professor in professores]

        return professores

    def update_usuario(self, usuario_to_be_updated: int, usuario_info_json: dict):

        usuario = self.create_usuario(usuario_info_json)
        usuario.usu_id = usuario_to_be_updated

        self.update_entity_with_commit(usuario)

    def delete_usuario(self, usuario_to_be_deleted: Usuario) -> None:
        
        self.delete_entity_with_commit(usuario_to_be_deleted)
       

    def get_alunos_by_ids(self, json: dict) -> list:
        alunos = self.session.query(Usuario).filter(Usuario.usu_id in json["alunos"]).all()
        return alunos

    def generate_radar_chart_report(self, id_projeto: int, id_usuario: int) -> dict:

        report_data = (self.session.query(Criterio.cri_nome, Nota.not_valor, Avaliacao.ava_avaliador,Avaliacao.ava_sprint,Usuario.usu_auth).
            join(
                Avaliacao, Nota.not_avaliacao == Avaliacao.ava_id
            ).join(
                Usuario, Avaliacao.ava_avaliador == Usuario.usu_id
            ).join(
                Criterio, Nota.not_criterio == Criterio.cri_id
            ).
            filter(
                and_(Avaliacao.ava_projeto == id_projeto, Avaliacao.ava_avaliado == id_usuario)
            )
        ).all()

        report_frame = pd.DataFrame(data=report_data,columns=('criterio','nota','avaliador_id','sprint','cargo'))
        report_grouped = self._group_avaliacao_by_sprint(report_frame, id_usuario)
        
        criterios = report_frame['criterio'].unique().astype(list)

        for sprint in report_grouped:
            radar_1 = self._generate_auto_avaliations_radar(sprint['autoavaliacao'],criterios)
            sprint['radar_1'] = radar_1

            radar_2 = self._generate_general_avaliations_radar(sprint['alunos'],sprint['professores'],criterios)
            sprint['radar_2'] = radar_2

        return report_grouped

    def _group_avaliacao_by_sprint(self,report: DataFrame, id_aluno: int) -> list:

        sprints_grouping = list()

        sprints = report['sprint'].unique().astype(list)


        for sprint in sprints:

            sprint_info = dict(
                nome = f'Sprint {sprint}',
                autoavaliacao = list(),
                alunos = list(),
                professores = list()
            )

            frame_by_sprint = report.query(f'sprint == {sprint}')

            for index, row in frame_by_sprint.iterrows():

                if row['avaliador_id'] == int(id_aluno):

                    sprint_info['autoavaliacao'].append({
                        row['criterio']:row['nota']
                    })

                elif row['cargo'] == 'Aluno':

                    sprint_info["alunos"].append({
                            row['criterio']:row['nota']
                        })

                elif row['cargo'] == 'Professor':

                    sprint_info["professores"].append({
                            row['criterio']:row['nota']
                        })            

            sprints_grouping.append(sprint_info)
        
        return sprints_grouping

    def _generate_auto_avaliations_radar(self, autoavaliacoes: list,criterios: list) ->list:

        criterios_soma = {criterio:0 for criterio in criterios}
        criterios_appear = {criterio:0 for criterio in criterios}

        for avaliacao in autoavaliacoes:

            keys = tuple(avaliacao.items())

            criterios_appear[keys[0][0]] += 1
            criterios_soma[keys[0][0]] += avaliacao[keys[0][0]]

        averages_criterios = list()

        for criterio, soma in criterios_soma.items():

            averages_criterios.append({
                "criterio":criterio,
                "nota": soma / criterios_appear.get(criterio,1)
            })

        return averages_criterios

    def _generate_general_avaliations_radar(self, avaliacoes_alunos: list,avaliacoes_professores: list,criterios: list) ->list:
        criterios_soma_aluno = {criterio:0 for criterio in criterios}
        criterios_appear_aluno = {criterio:0 for criterio in criterios}

        for avaliacao in avaliacoes_alunos:

            keys = tuple(avaliacao.items())

            criterios_appear_aluno[keys[0][0]] += 1
            criterios_soma_aluno[keys[0][0]] += avaliacao[keys[0][0]]

        criterios_soma_professor = {criterio:0 for criterio in criterios}
        criterios_appear_professor = {criterio:0 for criterio in criterios}

        for avaliacao in avaliacoes_professores:

            keys = tuple(avaliacao.items())

            criterios_appear_professor[keys[0][0]] += 1
            criterios_soma_professor[keys[0][0]] += avaliacao[keys[0][0]]

        averages_criterios = list()

        

        for criterio in criterios:
            averages_criterios.append({
                "criterio":criterio,
                "nota": (
                    (criterios_soma_aluno[criterio]/(criterios_appear_aluno[criterio] if criterios_appear_aluno[criterio] != 0 else 1)) +
                    (criterios_soma_professor[criterio]/(criterios_appear_professor[criterio] if criterios_appear_professor[criterio] != 0 else 1))
                    )/2
            })

        return averages_criterios
