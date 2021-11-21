from flask.json import jsonify
from dao.BaseDao import BaseDao
from models.Equipe import Equipe
from models.Projeto import Projeto
from dao.UsuarioDao import UsuarioDao
from models.Usuario import Usuario


class EquipeDao(BaseDao):

    def __init__(self) -> None:
        super().__init__()


    def convert_entity_to_dict(self,entity: Equipe, id_projeto = None) -> dict:
        usuario_dao = UsuarioDao()
        return {
            "equ_id":entity.equ_id,
            "equ_nome":entity.equ_nome,
            "equ_disciplina":entity.equ_disciplina,
            "equ_alunos":[usuario_dao.convert_entity_to_dict(aluno,id_projeto) for aluno in entity.alunos]
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

    def get_all_equipes_by_projeto(self, id_projeto: int):

        equipes = self.session.query(Equipe).all()
        equipes_in_projeto = list()

        for equipe in equipes:
            for projeto in equipe.projetos:
                if projeto.pro_id == id_projeto:
                    equipes_in_projeto.append(equipe) 
        return [self.convert_entity_to_dict(equipe,id_projeto) for equipe in equipes_in_projeto]        

    def get_all_equipes_by_disciplina(self,id_disciplina: int) -> list:

        equipes = self.session.query(Equipe).filter(Equipe.equ_disciplina == id_disciplina).all()

        equipes = [self.convert_entity_to_dict(equipe) for equipe in equipes]

        return equipes        

    def get_equipe_by_id(self, id_equipe: int) -> Equipe:

        equipe = self.session.query(Equipe).get(id_equipe)

        return equipe

    def update_equipe(self,equipe_to_be_updated: int, equipe_info_json: dict) -> None:

        equipe = self.create_equipe(equipe_info_json)
        equipe.equ_id = equipe_to_be_updated

        self.update_entity_with_commit(equipe)
        
    def delete_equipe(self, equipe_to_be_deleted: Equipe) -> None:

        self.delete_entity_with_commit(equipe_to_be_deleted)


    def create_equipe_alunos(self,json: dict) -> Equipe:
        return Equipe(
            equ_nome = json["nome"],
            equ_disciplina = json["disciplina"],
            equ_alunos = json["alunos"]
        )


    def define_alunos(self,json: dict) -> list:
        usuarioDao = UsuarioDao()

        entitys = []
        for id_usuario in json["alunos"]:
            entitys.append(usuarioDao.get_entity_by_id(id_usuario,Usuario))
        return entitys


    def update_equipe_alunos(self,equipe_to_be_updated: int, equipe_info_json: dict) -> None:
        equipe = self.get_equipe_by_id(equipe_to_be_updated)
        equipe.alunos = []
        self.update_entity_with_commit(equipe)
        equipe.alunos = self.define_alunos(equipe_info_json)
        self.update_entity_with_commit(equipe)
        

    def get_equipes_by_aluno(self, id_aluno: int) -> None:#list:
        usuario_dao = UsuarioDao()
        usuario = usuario_dao.get_entity_by_id(id_aluno, Usuario)
        equipes = []
        for equipe in usuario.equipes:
            equipes.append(equipe)

        return equipes