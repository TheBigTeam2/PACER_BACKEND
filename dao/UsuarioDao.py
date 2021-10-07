from dao.BaseDao import BaseDao
from models.Usuario import Usuario

class UsuarioDao(BaseDao):

    def __init__(self) -> None:
        super().__init__()

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
