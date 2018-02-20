from mightyMooc import app, db
from mightyMooc.backend.base_service import BaseService

class CourseService(BaseService):
    def __init__(self):
        self.model = 'Course'
        self.db_module = self.dyanmic_module()
        super(CourseService)


    def add_many_to_many(self, parent, children, relationship):
        ''' Build m-t-m records based on the relationship key
        :param: parent - mightyMooc.models object 
        :param: child - mightyMooc.models object 
        :param: relationship (str) - string of the relationship (e.g. 'institutions')
        '''
        self.many_to_many_map = {
        'institutions': parent.institutions,
        'modules': parent.modules,
        'users': parent.users,
        }  
        build_data = many_to_many_map.get(relationship)
        for child in children:
            build_data.append(child)
        db.session.commit()