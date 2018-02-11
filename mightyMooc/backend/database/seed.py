import ipdb

from mightyMooc import app, db
from mightyMooc.backend.user_service import UserService
from mightyMooc.backend.institution_service import InstitutionService
from mightyMooc.backend.module_service import ModuleService

class RunSeed():
	def __init__(self):
		users =[{'username': 'Michael Vaughn', 'email': 'mv@ecb.co.uk'},
		{'username': 'Marcus Trescothic', 'email': 'mt@ecb.co.uk'},	
		{'username': 'Mark Butcher', 'email': 'mb@ecb.co.uk' },
		{'username': 'Nasser Hussain', 'email': 'nh@ecb.co.uk'},
		{'username': 'Alec Stuart', 'email': 'as@ecb.co.uk' }]
		# self.generate(users, UserService, 'User')

		institutions =[{'name': 'Oxford'},
		{'name': 'Cambridge'},	
		{'name': 'Imperial',},
		{'name': 'Durham'},
		{'name': 'Bristol'}]
		# self.generate(institutions, InstitutionService, 'Institution')

		modules =[{'name': 'OOP'},
		{'name': 'Data structures'},	
		{'name': 'UI/UX',},
		{'name': 'Embedded Systems'},
		{'name': 'Databases'}]
		self.generate(modules, ModuleService, 'Module')

	@staticmethod
	def generate(data, import_object, model):
		create = 'create'
		for row in data:
			getattr(import_object(), create)(**row)
				

if __name__ == "__main__":
	RunSeed()
