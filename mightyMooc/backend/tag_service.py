from flask_restful_swagger import swagger

from mightyMooc import app, db
from mightyMooc.backend.base_service import BaseService
from mightyMooc.models import Tag, Course, Module
from mightyMooc.backend.institution_service import InstitutionService

class TagService(BaseService):
    def __init__(self):
        self.model = 'Tag'
        self.db_module = self.dyanmic_module()
        super(TagService)


    def get_modules_by_tag(self, tag):
        tags = Tag.query.filter(Tag.name.ilike(tag)).all()
        response = []
        for tag in tags: 
            response.append({'tag': tag.name, 'modules': 
                [m.name for m in tag.modules.all()]})
        return response
