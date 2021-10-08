from dao.BaseDao import BaseDao
from models.Usuario import Usuario

class UsuarioDao(BaseDao):

    def __init__(self) -> None:
        super().__init__()

    def convert_entity_to_dict(self,entity: Usuario) -> dict:
        
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
    
    def get_all_usuarios_by_professor(self) -> list:

        professores = self.session.query(Usuario).filter(Usuario.usu_auth == "Professor").all()

        professores = [self.convert_entity_to_dict(professor) for professor in professores]

        return professores
