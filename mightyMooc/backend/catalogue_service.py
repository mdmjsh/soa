
from flask_restful_swagger import swagger

from mightyMooc import app, db
from mightyMooc.models import Course, User 
from mightyMooc.backend.base_service import BaseService

class CatalogueService(BaseService):
	''' A service which retrieves hands items in the content catologue
	'''	
