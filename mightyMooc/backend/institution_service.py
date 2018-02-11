from mightyMooc import app, db
from mightyMooc.backend.base_service import BaseService

class InstitutionService(BaseService):
	def __init__(self):
		self.model = 'Institution'
		self.db_module = self.dyanmic_module()
		super(InstitutionService)

