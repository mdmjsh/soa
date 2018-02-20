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



    def add_many_to_many(self, parent, children, relationship):
        ''' Build m-t-m records based on the relationship key
        '''
        self.many_to_many_map = {
        'institutions': parent.institutions,
        'users': parent.users,
        }  
        build_data = many_to_many_map.get(relationship)
        for child in children:
            build_data.append(child)
        db.session.commit()
     
    def enrole(self, user_id, module_ids):
        ''' enrole a user to a module
            :param: module_ids - list of ids
        '''
        ipdb.set_trace()
        user = user_service.get_by_id_raw(user_id)
        modules = (self.get_by_id_raw(m_id) for m_id in module_ids)
        user.modules.extend(modules)
        db.session.commit()

