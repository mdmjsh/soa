import ipdb

from mightyMooc import app, db
from mightyMooc.backend.user_service import UserService
from mightyMooc.backend.institution_service import InstitutionService
from mightyMooc.backend.course_service CourseService
from mightyMooc.backend.module_service import ModuleService

def run_seed():
	print('RUNNING SEED!')
	users =[{'username': 'Michael Vaughn', 'email': 'mv@ecb.co.uk'},
	{'username': 'Marcus Trescothic', 'email': 'mt@ecb.co.uk'},	
	{'username': 'Mark Butcher', 'email': 'mb@ecb.co.uk' },
	{'username': 'Nasser Hussain', 'email': 'nh@ecb.co.uk'},
	{'username': 'Alec Stuart', 'email': 'as@ecb.co.uk' }]
	generate_data(users, UserService)

	institutions =[{'name': 'Oxford'},
	{'name': 'Cambridge'},	
	{'name': 'Imperial',},
	{'name': 'Durham'},
	{'name': 'Bristol'}]
	generate_data(institutions, InstitutionService)

	modules =[{'name': 'OOP'},
	{'name': 'Data structures'},	
	{'name': 'UI/UX',},
	{'name': 'Embedded Systems'},
	{'name': 'Databases'}]
	generate_data(modules, ModuleService)

	courses =[{'name': 'Software Engineering'},
	{'name': 'Web Design'},	
	{'name': 'Data Science Fundamentals',}]
	generate_data(courses, CoursesService)


def generate_data(data, import_class):
	for row in data:
		getattr(import_class(), 'create')(**row)

def delete_all():
	''' WIP not scalable need to dynamically load the tables
	'''
	u = UserService()
	users = u.get()
	ids = [user.id for user in users]
	for id in ids:
		u.delete(id)

	m = ModuleService()
	modules = m.get()
	ids = [module['id'] for module in modules]
	for id in ids:
		m.delete(id)

	i = InstitutionService()
	institutions = i.get()
	ids = [inst.id for inst in institutions]
	for id in ids:
		i.delete(id)
				

if __name__ == "__main__":
	delete_all()
	run_seed()
