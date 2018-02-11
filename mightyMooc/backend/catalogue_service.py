
from flask_restful_swagger import swagger

from mightyMooc import app, db
from mightyMooc.backend.module_service import ModuleService
from mightyMooc.backend.institution_service import InstitutionService

class CatalogueService():
  def __init__(self):
  	self.module_service = ModuleService()
  	self.institution_service = InstitutionService()


