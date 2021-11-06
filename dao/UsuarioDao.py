from sqlalchemy.sql.elements import and_
from dao.BaseDao import BaseDao
from models.Usuario import Usuario
from models.Avaliacao import Avaliacao

class UsuarioDao(BaseDao):

    def __init__(self) -> None:
        super().__init__()


    def get_avaliacoes_by_usuario_and_projeto(self,projeto: int, usuario_id: int):
        
        avaliacoes = self.session.query(Avaliacao).filter(and_(Avaliacao.ava_projeto == projeto,Avaliacao.ava_avaliador == usuario_id)).all()

        return [avaliacao.as_dict() for avaliacao in avaliacoes]

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
            usu_rg = json["rg"],
            usu_cpf = json["cpf"],
            usu_nome = json["nome"],
            usu_auth = json["auth"]

        )

    def save_usuario(self,object):

        entitys = self.create_usuario(object)

        return self.save_entity_with_commit(entitys)

    def get_all_usuarios_by_aluno(self) -> list:

        alunos = self.session.query(Usuario).filter(Usuario.usu_auth == "Aluno").all()

        alunos = [self.convert_entity_to_dict(aluno) for aluno in alunos]

        return alunos


    def get_all_alunos(self) -> list:
        alunos = self.session.query(Usuario).filter(Usuario.usu_auth == "Aluno").all()

        return alunos

    
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
