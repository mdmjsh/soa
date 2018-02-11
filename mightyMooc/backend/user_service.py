from flask_restful_swagger import swagger
from flask_login import current_user, login_user, logout_user, login_required

from mightyMooc import app, db
from mightyMooc.backend.base_service import BaseService

class UserService(BaseService):
	def __init__(self):
		self.model = 'User'
		self.db_module = self.dyanmic_module()
		super(User)

