from mightyMooc import app, db
from mightyMooc.backend.base_service import BaseService

class TagService(BaseService):
	def __init__(self):
		self.model = 'Tag'
		self.db_module = self.dyanmic_module()
		super(TagService)