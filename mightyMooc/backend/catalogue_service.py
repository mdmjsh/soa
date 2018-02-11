
from flask_restful_swagger import swagger

from mightyMooc import app, db
from mightyMooc.models import Course, User, Module, Institution 
from mightyMooc.backend.base_service import BaseService

class CatalogueService(BaseService):
  def __init__(self):
    self.model = 'User'
    self.db_module = self.dyanmic_module()
    super(User)
