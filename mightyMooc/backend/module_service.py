import ipdb
from flask import current_app
from mightyMooc import app, db
from mightyMooc.backend.base_service import BaseService


class ModuleService(BaseService):
    def __init__(self):
        self.model = 'Module'
        self.db_module = self.dyanmic_module()
        super(ModuleService)

    def add_many_to_many(self, parent, children, relationship):
    	''' Build m-t-m records based on the relationship key
    	'''
    	router = {
		'institutions': parent.institutions,
		}

    	build_data = router.get(relationship)
    	for child in children:
    		build_data.append(child)
    	db.session.commit()


            