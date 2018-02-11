from flask_restful_swagger import swagger

from mightyMooc import app, db
from mightyMooc.backend.base_service import BaseService

class ContentProvider(BaseService):
	def __init__(self):
		self.model = 'ContentProvider'
		self.db_module = self.dyanmic_module()
		super(ContentProvider)