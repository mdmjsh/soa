from flask_restful_swagger import swagger

from mightyMooc import app, db
from mightyMooc.backend.base_service import BaseService
from mightyMooc.backend.module_service import ModuleService
from mightyMooc.backend.course_service import CourseService
from mightyMooc.backend.institution_service import InstitutionService

class CatalogueService(BaseService):
	'''
		A service for querying the whole mightyMooC catalogue
		adding module/course content, and 
		for students to enrole on modules/courses
	'''
  def __init__(self):
  	module_service = ModuleService()
  	institution_service = InstitutionService()

############ GET ##########################

	def get_by_tags(self, tags):
		'''
		:param: tags: list of strings of tags to include
		:returns: JSON response of courses and modules matching the tags
		'''
		modules = module_service.get(**{'tags': tags})
		courses = cour



  	#by_category
	#name
	#by_user
	#by_provider 
	#by_id

############# POST ##########################

# enrole: user_id, course_id 
# Update
# upload modules




