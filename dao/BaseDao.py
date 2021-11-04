from abc import ABC,abstractmethod
from utils.SingleSession import SingleSession

class BaseDao(ABC):

    def __init__(self) -> None:
        self.session = SingleSession.get_session()

    def __del__(self) -> None:
        print('fechando')
        self.session.close()

    def save(self,object):
        
        try:
            self.session.add(object)
            return True
        
        except Exception as error:
            print(error)
            return False
    
    def update(self, object):
        try:
            self.session.merge(object)
            return True
        
        except Exception as error:
            print(error)
            return False

    def delete(self, object):
        try:
            self.session.delete(object) 
            return True
        
        except Exception as error:
            print(error)
            return False


    def delete_entity_with_commit(self, object) -> bool:
        is_deleted = self.delete(object)

        if is_deleted:
            self.session.commit()
        else:
            self.session.rollback()

        return is_deleted

    def update_entity_with_commit(self, object) -> bool:
        is_updated = self.update(object)

        if is_updated:
            self.session.commit()
        else:
            self.session.rollback()

        return is_updated

    def save_entity_with_commit(self, object) -> bool:
        is_saved = self.save(object)

        if is_saved:
            self.session.commit()
        else:
            self.session.rollback()

        return is_saved

    def save_entity_in_mass(self, collection: list) -> bool:
        db_insertions = [self.save_entity_with_commit(item) for item in collection]

        if all(is_saved for is_saved in db_insertions):
            self.session.commit()
            return True
        
        else:
            self.session.rollback()
            return False

    def get_entity_by_id(self, id_equipe: int, object_type):

        entity = self.session.query(object_type).get(id_equipe)

        return entity