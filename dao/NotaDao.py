from dao.BaseDao import BaseDao
from models.Nota import Nota

class NotaDao(BaseDao):

    def __init__(self) -> None:
        super().__init__()

    def save_nota(self,object: Nota) -> bool:

        is_saved = self.save(object)
        if is_saved:
            self.session.commit()
        else:
            self.session.rollback()

        return is_saved

    def save_notas_in_mass(self, notas_collection: list(Nota)):

        db_insertions = [self.save(nota) for nota in notas_collection]

        if all(is_saved for is_saved in db_insertions):
            self.session.commit()
            return True
        
        else:
            self.session.rollback()
            return False
