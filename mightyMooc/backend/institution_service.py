import ipdb
from mightyMooc import app, db
from mightyMooc.models import Institution
from mightyMooc.backend.base_service import BaseService
from mightyMooc.backend.course_service import CourseService

course_service = CourseService()

class InstitutionService(BaseService):
    def __init__(self):
        self.model = 'Institution'
        self.db_module = self.dyanmic_module()
        super(InstitutionService)

    def build_institution_json(self, name):
        ''' Build a dictionary for all courses that an institution provides
            content for
        '''
        institutions = Institution.query.filter(
            Institution.name.ilike(name)).all()
        for institution in institutions:
            response = []
            for course in institution.courses.all():
                response.append(self.json_institution_course_modules(
                    course, institution))
        return response


    def json_institution_course_modules(self, course, institution):
        ''' Find all modules and courses offered to by a given institution and 
            build a JSON response
            
            :param: institution - mightyMooC models object 
            :param: course - mightyMooC models object 
        '''
        module_data = [] 
        for module in course.modules:
            if self.check_publisher(module, institution.name):
                module_data.append(
                    {'id': module.id, 
                    'module': module.name, 
                    'description': module.description,
                    'tags': [tag.name for tag in module.tags]}
                )
        response =  {
                'course': course.name, 
                'id': course.id,
                'modules': module_data, 
        }
        return response




