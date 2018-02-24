import ipdb
from mightyMooc import app, db
from mightyMooc.backend.base_service import BaseService
from mightyMooc.backend.module_service import ModuleService
from mightyMooc.backend.user_service import UserService

module_service = ModuleService()
user_service = UserService()

class CourseService(BaseService):
    def __init__(self):
        self.model = 'Course'
        self.db_module = self.dyanmic_module()
        super(CourseService)


    def add_many_to_many(self, parent, children, relationship):
        ''' Build m-t-m records based on the relationship key
        :param: parent - mightyMooc.models object 
        :param: child - mightyMooc.models object 
        :param: relationship(str) - string of the relationship
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

    def enrole(self, user_id, course_id):
        ''' enrole a user to a course
            cascades to enrole them on every module in the course

            Currently built for one course id (even though a list)
            easily extendable to use multiple.
        '''
        user = user_service.get_by_id_raw(user_id)
        course = self.get_by_id_raw(course_id[0])
        module_ids = [module.id for module in course.modules]
        user.courses.append(course)
        module_service.enrole(user_id, module_ids)
        try:
            db.session.commit()
            return self.build_enrolement_json(course, user)
        except: 
            db.session.rollback()
            return {'status': 500, 'message': 'Something went wrong'}


    def build_enrolement_json(self, course, user):
        ''' Find all modules and courses subscribed to by a given user and 
            build a JSON response
            
            :param: user - mightyMooC models object 
            :param: course - mightyMooC models object 
        '''
        module_data = [] 
        for module in course.modules:
            module_data.append(
                {'id': module.id, 
                'module': module.name, 
                'description': module.description,
                'tags': [tag.name for tag in module.tags]}
            )
        response =  {
                'user_name': user.username,
                'course': course.name, 
                'id': course.id,
                'modules': module_data, 
        }
        return response







