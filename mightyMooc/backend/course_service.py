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


    def enrol(self, user_id, course_id):
        ''' enrol a user to a course
            cascades to enrol them on every module in the course

            Currently built for one course id (even though a list)
            easily extendable to use multiple.
        '''
        user = user_service.get_by_id_raw(user_id)
        course = self.get_by_id_raw(course_id[0])
        module_ids = [module.id for module in course.modules]
        user.courses.append(course)
        module_service.enrol(user_id, module_ids)
        try:
            db.session.commit()
            return self.build_enrollment_json(course, user)
        except: 
            db.session.rollback()


    def build_enrollment_json(self, course, user):
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







