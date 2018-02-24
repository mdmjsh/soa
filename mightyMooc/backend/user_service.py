import ipdb
from flask_restful_swagger import swagger
from flask_login import current_user, login_user, logout_user, login_required

from mightyMooc import app, db
from mightyMooc.backend.base_service import BaseService

class UserService(BaseService):
    def __init__(self):
        self.model = 'User'
        self.db_module = self.dyanmic_module()
        super(UserService)

    def get_by_id(self, id):
        remove_keys = ['password_hash', 'email', 'last_sign_in', 'user_type']
        user = self.db_module.query.filter_by(id=id).first()
        self.results = [user]
        response = self.to_results(remove_keys=remove_keys)
        response[0]['courses'] = [course.name for course in user.courses]
        response[0]['modules'] = [module.name for module in user.modules]
        return {"status": "ok", "data": response}