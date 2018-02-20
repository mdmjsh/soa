import ipdb
from flask_restful_swagger import swagger

from mightyMooc import app, db
from mightyMooc.backend.base_service import BaseService
from mightyMooc.backend.module_service import ModuleService
from mightyMooc.backend.course_service import CourseService
from mightyMooc.backend.institution_service import InstitutionService
from mightyMooc.backend.tag_service import TagService

class CatalogueService(BaseService):
    '''
        A service for querying the whole mightyMooC catalogue
        adding module/course content, and 
        for students to enrole on modules/courses
    '''
    def __init__(self):
        self.tag_service = TagService()
        self.module_service = ModuleService()
        self.institution_service = InstitutionService()
        self.course_service = CourseService()

############ GET ##########################

    def get(self, **kwargs):
        '''
        Returns a module, course, or institution by the given id
        '''
        if kwargs.get('type') == 'course':
            return self.course_service.get_by_id(kwargs.get('id'))
        elif kwargs.get('type') == 'module': 
            return self.module_service.get_by_id(kwargs.get('id'))
        elif kwargs.get('type') == 'institution':
            return self.institution_service.get_by_id(kwargs.get('id'))
        else:
            return({'error': '404 - {} resource not found'.format(kwargs.get('type'))})

    def get_tags(self, tag):
        '''
        :param: tag: string
        :returns: JSON response of courses and modules matching the tag
        '''
        return self.tag_service.get_modules_by_tag(tag)

    def get_institutions(self, institution):
        '''
        :param: institution: string
        :returns: JSON response of courses and modules matching the institution
        '''
        return self.institution_service.get_courses_and_modules(institution)







    #by_user

############# POST ##########################

# enrole: user_id, course_id 
# Update
# upload modules




