'''
Mimics rake db drop create migrate 
DANGER!!!! will completely destroy your database - never suitable for production!!!!!! 
(Unless you really want to get rid of something incriminating quickly)
'''
import ipdb
import os
import mightyMooc.models as models

from flask import Flask, current_app
from sqlalchemy import MetaData
from mightyMooc import app, db
from mightyMooc.backend import module_service, user_service, institution_service, course_service
from mightyMooc.database.seed import RunSeed

	
def destroy(engine, meta):
	'''	Remove all table content but keep schema
		REF: https://gist.github.com/absent1706/3ccc1722ea3ca23a5cf54821dbc813fb
	''' 
	print('Clearing data')
	meta = MetaData(bind=engine, reflect=True)
	con = engine.connect()
	trans = con.begin()
	for table in meta.sorted_tables:
	    con.execute(table.delete())
	trans.commit()

def delete():
	''' WIP not scalable need to dynamically load the tables
	'''
	print('deleting data...')
	u = user_service.UserService()
	delete = u.get_raw()
	ids = [user.id for user in users]
	for id in ids:
		models.User.query.filter(models.User.id == id).delete()


	m = module_service.ModuleService()
	modules = m.get_raw()
	ids = [module.id for module in modules]
	for id in ids:
		models.Module.query.filter(models.Module.id == id).delete()

	i = institution_service.InstitutionService()
	institutions = i.get_raw()
	ids = [inst.id for inst in institutions]
	for id in ids:
		models.Institution.query.filter(models.Institution.id == id).delete()


	courses = course_service.CourseService()
	course_services = cs.get_raw()
	ids = [course_serv.id for course_serv in course_services]
	for id in ids:
		models.CourseService.query.filter(models.CourseService.id == id).delete()


	cs = course_service.CourseService()
	course_services = cs.get_raw()
	ids = [course_serv.id for course_serv in course_services]
	for id in ids:
		models.CourseService.query.filter(models.CourseService.id == id).delete()
# 
	db.session.commit()
	print('Done')


def migrate(): 
	db.create_all()
	# os.system("cd /Users/fionatout/Documents/Oxford/first_year/SOA/code/mightyMooc/")
	# os.system("flask db migrate && flask db upgrade")

def seed():
	RunSeed()

if __name__ == '__main__':
	# if os.environ['MODE'] == 'DEVELOPMENT':
	# TODO: uncomment these check one the application is in a docker container
	with app.test_request_context():
		engine = db.engine
		meta = MetaData()
		meta.reflect(engine)
		destroy(engine, meta)
		# delete()
		migrate()
		seed()
		print('Done')
	# else: 
	# 	print('No way son!')
