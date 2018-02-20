import importlib
import copy

import mightyMooc.models

from datetime import datetime
from sqlite3 import IntegrityError
from sqlalchemy import exc
from mightyMooc import app, db
from flask import jsonify, request, make_response
import ipdb

class BaseService():

    def __init__(self):
        self.db_module = self.dyanmic_module()

# # # # # # # # # # HELPER METHODS # # # # # # # # # # # # # # # # # # # # # 

    def dyanmic_module(self):
        ''' Dynmically load the relevant class from mightMooc.models 
        '''
        mod = __import__('mightyMooc.models', fromlist=[str(self.model)])
        db_module = getattr(mod, str(self.model))
        return db_module


    def print_kwargs(self, method, kwargs):
        print ('{} {} object with data: {}'.format(method, self.db_module, ','
            .join(['{}: {}'.format(k, v) for k, v in kwargs.items()])))

    def __len__(self):
        return len(self.get())

    def to_results(self):
        '''
        iterate over the list of objects results from original sqlalchemy call 
        remove unwanted keys from the results
        append the cleaned results to a list of dicts
        '''
        REMOVE_KEYS = ['_sa_instance_state', 'deleted_at']
        results = []
        for result_set in self.results:
            #  Make a copy as we are muting and iterating
            result_dict = copy.copy(vars(result_set)) 
            for remove_key in REMOVE_KEYS:
                del result_dict[remove_key] 
            result_dict['created_at'] = str(result_dict['created_at'])
            result_dict['updated_at'] = str(result_dict['created_at'])
            results.append(result_dict)
        # results.append({'total': len(result_dict) if result_dict else 0})
        return results

# # # CRUD METHODS # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
    def create(self, **kwargs):
        kwargs['created_at'] = datetime.now()
        data = self.db_module(**kwargs)
        db.session.merge(data)
        try:
            db.session.commit()
            return self.get_raw(**kwargs)[0]
        except exc.IntegrityError as e:
            db.session.rollback()
            print('IntegrityError')

    def get(self, **kwargs):        
        self.results = self.db_module.query.filter_by(**kwargs).all() 
        return make_response(jsonify({"status": "ok", "data": 
            self.to_results()}), 200)

    def get_raw(self, **kwargs):
        ''' Returns raw data db level data not jsonified
        '''     
        return self.db_module.query.filter_by(**kwargs).all() 

    def get_by_id(self, id):
        self.results = [self.db_module.query.filter_by(id=id).first()]
        return self.to_results()

    def get_by_id_raw(self, id):
        return self.db_module.query.filter_by(id=id).first()

    def update(self, id, **kwargs):
        self.print_kwargs('Updating', kwargs)
        row = self.get_by_id(id)
        kwargs['updated_at'] = datetime.now()
        for key, value in kwargs.items():
            setattr(row, key, value)
        db.session.commit()

    def delete(self, id):
        row = self.get_by_id(id)
        print('Deleting {}'.format(row))
        
        User.query.filter(User.id == id).delete()
        db.session.delete(row)























