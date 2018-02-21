from flask_rbac import RoleMixin
from mightyMooc import app, db

class Role(RoleMixin):
    pass

anonymous = Role('anonymous')