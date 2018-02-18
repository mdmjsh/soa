from flask_restful_swagger import swagger

from mightyMooc import app, db
from mightyMooc.backend.module_service import ModuleService
from mightyMooc.backend.institution_service import InstitutionService

class TagService():
    def __init__(self):
        self.model = 'Tag'
        self.db_module = self.dyanmic_module()
        super(TagService)

