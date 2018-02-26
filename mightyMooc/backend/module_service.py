import ipdb
import copy
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
     
    def enrol(self, user_id, module_ids):
        ''' enrol a user to a module
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

    def to_results(self, remove_keys=None):
        '''
        Iterate over the list of raw results.  
        Remove unwanted keys from the results.
        Append the cleaned results to a list of dicts. 
        :param: remove_keys - custom list of additional keys remove
        '''
        REMOVE_KEYS = ['_sa_instance_state', 'deleted_at',
        'created_at', 'updated_up']
        if remove_keys:
            REMOVE_KEYS += remove_keys
        results = []
        for result_set in self.results:
            #  Make a copy as we are iterating the data we are mutating
            result_dict = copy.copy(vars(result_set)) 
            for remove_key in REMOVE_KEYS:
                del result_dict[remove_key] 
            result_dict['institutions'] = [i.name for i in 
                                           result_set.institutions.all()]
            result_dict['courses'] = [c.name for c in 
                                      result_set.courses.all()]
            result_dict['tags'] = [t.name for t in 
                                    result_set.tags.all()]
            results.append(result_dict)
        return results
