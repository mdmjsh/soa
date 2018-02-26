import importlib
import copy

import mightyMooc.models

from datetime import datetime
from sqlite3 import IntegrityError
from sqlalchemy import exc
from mightyMooc import app, db
from flask import jsonify, request, make_response, abort
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

    def to_results(self, remove_keys=None):
        '''
        Iterate over the list of raw results.  
        Remove unwanted keys from the results.
        Append the cleaned results to a list of dicts. 

        :param: remove_keys - custom list of additional keys remove
        '''
        REMOVE_KEYS = ['_sa_instance_state', 'deleted_at',
        'created_at', 'updated_up']
        if remove_keys:
            REMOVE_KEYS += remove_keys
        results = []
        for result_set in self.results:
            #  Make a copy as we are iterating the data we are mutating
            result_dict = copy.copy(vars(result_set)) 
            for remove_key in REMOVE_KEYS:
                del result_dict[remove_key] 
            results.append(result_dict)
        return results

    def add_many_to_many(self, parent, children, relationship):
        ''' Build m-t-m records based on the relationship key
        '''
        many_to_many_map = {
        'institutions': parent.institutions,
        'users': parent.users,
        'courses': parent.courses
        }  
        build_data = many_to_many_map.get(relationship)
        for child in children:
            build_data.append(child)
        db.session.commit()
        return build_data


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
        ''' Query model and return jsonified repsonse
        '''  
        kwargs['deleted_at'] = None   
        self.results = self.db_module.query.filter_by(**kwargs).all() 
        return {"status": "ok", "data": self.to_results()}

    def get_raw(self, **kwargs):
        ''' Returns raw, unjsonified db level data
        '''     
        return self.db_module.query.filter_by(**kwargs).all() 

    def get_by_id(self, id):
        self.results = [self.db_module.query.filter_by(id=id).first()]
        return {"status": "ok", "data": self.to_results()}

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


    def soft_delete(self, type, id, requestor_id, deleted_by):
        ''' Soft delete an item by setting its deleted at timestamp. 
            If the requestor_id does not have permission for the deletion 
            a 403 will be raised
            :param: type - type of item to delete 
            :param: id - id of item to delete
            :param: requestor_id - id party requesting the deletion
                e.g. 'modules'
            :param: deleted_by: str - string of the type of user attempting to 
                    make the soft delete. e.g. 'institution / 'student'
        '''
        to_delete = self.get_by_id_raw(id)
        delete_dict = {'student': to_delete.users.all(), 
                       'institution': to_delete.institutions.all(), 
        }
        approved = [m.id for m in to_delete.users.all()]
        if requestor_id in approved:
            print('Soft deleting {}'.format(to_delete.name))
            to_delete.deleted_at = datetime.now()
            db.session.merge(to_delete)
            return{'status': 200, 'to_delete': to_delete.name, 
                    'message': 'Our administrators will get back to you shortly'}
        else: 
            abort(403)












