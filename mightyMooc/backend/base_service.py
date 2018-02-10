import importlib

import mightyMooc.models

from datetime import datetime
from flask_restful_swagger import swagger
from mightyMooc import app, db
import ipdb

class BaseService(object):

	def __init__(self, model):
		self.model = model
		self.db_module = self.dyanmic_module()

# # # HELPER METHODS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

	def dyanmic_module(self):
		''' Dynmically load the relevant class from mightMooc.models 
		'''
		mod = __import__('mightyMooc.models', fromlist=[str(self.model)])
		db_module = getattr(mod, str(self.model))
		return db_module


	def print_kwargs(self, method, kwargs):
		print ('{} {} object with data: {}'.format(method, self.db_module, ','.join(
			['{}: {}'.format(k, v) for k, v in kwargs.items()])))

	def __len__(self):
		return len(self.get())

# # # CRUD METHODS # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
	
	def create(self, **kwargs):
		self.print_kwargs('Creating', kwargs)
		kwargs['created_at'] = datetime.now()
		data = self.db_module(**kwargs)
		db.session.add(data)
		db.session.commit()
		print('done')

	def get(self, **kwargs):
		return self.db_module.query.filter_by(**kwargs).all()		

	def get_by_id(self, id):	
		return self.db_module.query.filter_by(id=id).first()

	def update(self, id, **kwargs):
		self.print_kwargs('Updating', kwargs)
		row = self.get_by_id(id)
		kwargs['updated_at'] = datetime.now()
		for key, value in kwargs.items():
			ipdb.set_trace()
			setattr(row, key, value)
		db.session.commit()

	def delete(self, id):
		row = self.get_by_id(id)
		print('Deleting {}'.format(row))
		db.session.delete(row)

























