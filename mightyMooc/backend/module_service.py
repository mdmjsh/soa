import ipdb
from flask import current_app
from mightyMooc import app, db
from mightyMooc.backend.base_service import BaseService
from mightyMooc.backend.user_service import UserService

user_service = UserService()

class ModuleService(BaseService):
    def __init__(self):
        self.model = 'Module'
        self.db_module = self.dyanmic_module()
        super(ModuleService)
     
    def enrole(self, user_id, module_ids):
        ''' enrole a user to a module
            :param: module_ids - list of ids
        '''
        user = user_service.get_by_id_raw(user_id)
        modules = set()
        for m_id in set(module_ids): 
            modules.add(self.get_by_id_raw(m_id))
        user.modules.extend(modules)
        module_names = [module.name for module in user.modules]
        try:
            db.session.commit()
            return {'username': user.username, 'modules': module_names}
        except: 
            db.session.rollback()

