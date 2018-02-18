from flask import current_app
from mightyMooc import app, db
from mightyMooc.backend.base_service import BaseService

class ModuleService(BaseService):
    def __init__(self):
        self.model = 'Module'
        self.db_module = self.dyanmic_module()
        super(ModuleService)


            