from dao.BaseDao import BaseDao
from models.Projeto import Projeto
from dao.DisciplinaDao import DisciplinaDao

class ProjetoDao(BaseDao):

    def __init__(self) -> None:
        super().__init__()

    def convert_entity_to_dict(self,entity: Projeto) -> dict:
        disciplina_dao = DisciplinaDao()
        return {
            "pro_id":entity.pro_id,
            "pro_tema":entity.pro_tema,
            "pro_inicio":str(entity.pro_inicio),
            "pro_termino":str(entity.pro_termino),
            "disciplinas": [disciplina_dao.convert_entity_to_dict(disciplina) for disciplina in entity.disciplinas]
        }

    def create_projeto(self,json: dict) -> Projeto:
        disciplina_dao = DisciplinaDao()
        return Projeto(
            pro_tema = json["pro_tema"],
            pro_inicio = json["pro_inicio"],
            pro_termino = json["pro_termino"],
            disciplinas = [disciplina_dao.get_disciplina_by_id(disciplina["dis_id"]) for disciplina in json["disciplinas"]]
        )

    def save_projeto(self,object):

        entitys = self.create_projeto(object)

        return self.save_entity_with_commit(entitys)

    def get_all_projetos(self) -> list:

        projetos = self.session.query(Projeto).all()

        projetos = [self.convert_entity_to_dict(projeto) for projeto in projetos]

        return projetos
    
    def get_projeto_by_id(self, id_projeto: int) -> Projeto:

        projeto = self.session.query(Projeto).get(id_projeto)
        print(self.convert_entity_to_dict(projeto))
        return projeto
    
    def update_projeto(self,projeto_to_be_updated: int, projeto_info_json: dict) -> None:

        projeto = self.create_projeto(projeto_info_json)
        projeto.pro_id = projeto_to_be_updated

        self.update_entity_with_commit(projeto)
    
    def delete_projeto(self,projeto_to_be_deleted: int) -> None:
        
        projeto = self.get_projeto_by_id(projeto_to_be_deleted)

        return self.delete_entity_with_commit(projeto)


    ## RELACIONANDO PROJETOS E EQUIPES

    def buscar_projetos_da_equipe(self, idEquipe):
        projetos = self.session.query(Projeto).all()

        projetosFiltrados = []

        for projeto in projetos:
            equipes = projeto.equipes
            equipePertence = False
            for equipe in equipes:
                print(equipe.equ_id, idEquipe)
                if int(equipe.equ_id) == int(idEquipe):
                    equipePertence = True
            if equipePertence:
                projetosFiltrados.append(projeto.as_dict())

        return projetosFiltrados

    def atribuir_projeto_equipe(self, entitys, id_equipe: int) -> list:
        from dao.EquipeDao import EquipeDao
        equipe_dao = EquipeDao()
        equipe = equipe_dao.get_equipe_by_id(id_equipe)
        if equipe:
            entitys.append(equipe)
            return entitys
        else:
            return entitys


    def incluir_projeto_equipe(self, json: dict) -> None:
        projeto = self.get_projeto_by_id(json["projeto"])
        entitys = []
        if projeto.equipes:
            for equipe_previa in projeto.equipes:
                entitys.append(equipe_previa)

        projeto.equipes = self.atribuir_projeto_equipe(entitys, json["equipe"])
        return self.update_entity_with_commit(projeto)


    def substituir_projeto_equipe(self, json:dict) -> None:
        projeto = self.get_projeto_by_id(json["projeto"])
        if projeto:
            entitys = []
            projeto.equipes = self.atribuir_projeto_equipe(entitys, json["equipe"])
            return self.update_entity_with_commit(projeto)


    def remover_projeto_equipe(self, json:dict) -> None:
        from dao.EquipeDao import EquipeDao
        projeto = self.get_projeto_by_id(json["projeto"])
        if projeto and projeto.equipes:
            equipe_dao = EquipeDao()
            equipe = equipe_dao.get_equipe_by_id(json["equipe"])
            if equipe in projeto.equipes:
                projeto.equipes.remove(equipe)
                return self.update_entity_with_commit(projeto)
            else:
                return 404
        else:
            return 404

    def buscar_sprints_do_projeto(self, projeto):
        from models.Avaliacao import Avaliacao
        sprints = []
        for row in self.session.query(Avaliacao.ava_sprint).distinct(Avaliacao.ava_sprint).filter(Avaliacao.ava_projeto == projeto).all():
            sprints.append(row[0])
        return sprints