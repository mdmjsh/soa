from mightyMooc import app, db
from mightyMooc.backend.base_service import BaseService

class CourseService(BaseService):
	def __init__(self):
		self.model = 'Course'
		self.db_module = self.dyanmic_module()
		super(CourseService)