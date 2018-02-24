import ipdb
from flask import request, current_app, jsonify

from webargs import fields
from webargs.flaskparser import use_args

from mightyMooc import app, db
from mightyMooc.backend.module_service import ModuleService
from mightyMooc.backend.course_service import CourseService
from mightyMooc.backend.institution_service import InstitutionService
from mightyMooc.backend.user_service import UserService

course_service = CourseService()
module_service= ModuleService()
institution_service= InstitutionService()
user_service= UserService()

SERVICE_ROUTER = {
    'module': module_service,
    'course': course_service
}

@app.route('/catalogue', methods=['GET'])
def catalogue():
    kwargs = request.args.to_dict()
    return jsonify(catalogue_service.get(**kwargs))


@app.route('/catalogue/tags/<string:tag>', methods=['GET'])
def get_by_tag(tag):
    return jsonify(catalogue_service.get_tags(tag))

@app.route('/catalogue/institutions/<string:institution>', methods=['GET'])
def get_by_institution(institution):
    return jsonify(catalogue_service.get_institutions(institution))


@app.route('/catalogue/<string:type>/<int:id>', methods=['GET'])
def get_by_id(type, id):
    return jsonify(catalogue_service.get_by_id(**{'type': type, 'id': id}))


@app.route('/catalogue/add', methods=['POST'])
def add_content():
    ''' Used to add a new module or course to the catalogue
    '''
    request_data = request.get_json()
    service = SERVICE_ROUTER.get(request_data.get('type'))
    institutions = [institution_service.get_by_id_raw(request_data[
        'institution_id'])]
    ipdb.set_trace()
    del(request_data['type'])
    del(request_data['institution_id'])
    result = service.create(**request_data)
    service.add_many_to_many(result, institutions, 'institutions')
    return jsonify({'message': 'data added successfully', 'data': request_data,
     'status': 200})


# @app.route('/catalogue/<string:type>/<int:id>/<int:institution_id>', 
#     methods=['DELETE'])
# def soft_delete(type, id, institution_id):
#     ''' 
#     '''
#     service.soft_delete(type, id, institution_id)


@app.route('/catalogue/enrole', methods=['POST'])
def enrolement():
    '''  Used to enrole a user on a module or course
        :param: content_id - maps to a module or course depending on type param
        :param: type - string - 'module' or 'course' 
    '''
    request_data = request.get_json()
    service = SERVICE_ROUTER.get(request_data.get('type'))
    response = service.enrole(request_data['user_id'], 
        request_data['content_ids'])
    return jsonify({'message': 'data added successfully', 'data': response,
     'status': 200})

@app.route('/catalogue/students/<int:id>', methods=['GET'])
def student(id):
    ''' Fetch a users enrolements 
    '''
    return jsonify(user_service.get_by_id(id))










