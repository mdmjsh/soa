from mightyMooc import app, db
from mightyMooc.models import Institution
from mightyMooc.backend.base_service import BaseService


class InstitutionService(BaseService):
    def __init__(self):
        self.model = 'Institution'
        self.db_module = self.dyanmic_module()
        super(InstitutionService)

    def get_courses_and_modules(self, institution):
        institutions = Institution.query.filter(
            Institution.name.ilike(institution)).all()
        response = []
        for institution in institutions:

            response.append({'institution': institution.name, 
                'modules': [m.name for m in institution.modules.all()],
                'courses': [c.name for c in institution.courses.all()]
                })
        return response

