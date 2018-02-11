'''
Mimics rake db drop create migrate 
DANGER!!!! will completely destroy your database - never suitable for production!!!!!! 
(Unless you really want to get rid of something incriminating quickly)
'''
import os
from sqlalchemy import MetaData
from mightyMooc import app, db
from mightyMooc.backend import module_service, user_service, institution_service
from mightyMooc.backend.database.seed import RunSeed

	
def destroy(engine, meta):
	tables = (table.name for table in meta.tables.values() if table.name != 'alembic_version')
	for tablename in tables: 
		print('deleting {}'.format(tablename))
		db.delete(tablename)
	print('they\'re all gone now')

def delete():
	''' WIP not scalable need to dynamically load the tables
	'''
	u = user_service.UserService()
	users = u.get()
	ids = [user.id for user in users]
	for id in ids:
		u.delete(id)


	m = module_service.ModuleService()
	modules = m.get()
	ids = [module.id for module in modules]
	for id in ids:
		m.delete(id)

	i = institution_service.InstitutionService()
	institutions = i.get()
	ids = [inst.id for inst in institutions]
	for id in ids:
		i.delete(id)


def migrate(): 
	db.create_all()
	# os.system("cd /Users/fionatout/Documents/Oxford/first_year/SOA/code/mightyMooc/")
	# os.system("flask db migrate && flask db upgrade")

def seed():
	RunSeed()

if __name__ == '__main__':
	# if os.environ['MODE'] == 'DEVELOPMENT':
	# TODO: uncomment these check one the application is in a docker container
	engine = db.engine
	meta = MetaData()
	meta.reflect(engine)
	# destroy(engine, meta)
	delete()
	migrate()
	seed()
	print('Done')
	# else: 
	# 	print('No way son!')
