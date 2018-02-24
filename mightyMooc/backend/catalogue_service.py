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
        self.CATALOGUE_ROUTER = {
        'course': self.course_service,
        'module': self.module_service, 
        'institution': self.institution_service,
        }

############ GET ##########################

    def get(self, **kwargs):
        '''
        Returns a module, course, or institution by the given id
        '''
        # try:
        service = self.CATALOGUE_ROUTER.get(kwargs['type'])
        del(kwargs['type'])
        return service.get(**kwargs)
        # except:
        #     return({'status': 'error', 'message': 'resource not found: {}'.
        #         format(kwargs.get('type'))})


    def get_by_id(self, **kwargs):
        '''
        Returns a module, course, or institution by the given id
        '''
        try:
            service = self.CATALOGUE_ROUTER.get(kwargs['type'])
            return service.get_by_id(kwargs.get('id'))
        except:
            return({'error': '404 - {} resource not found'.format(
                kwargs.get('type'))})

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







