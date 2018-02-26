import ipdb
from flask import request, current_app, jsonify

from webargs import fields
from webargs.flaskparser import use_args

from mightyMooc import app, db
from mightyMooc.backend.catalogue_service import CatalogueService
from mightyMooc.backend.module_service import ModuleService
from mightyMooc.backend.course_service import CourseService
from mightyMooc.backend.institution_service import InstitutionService
from mightyMooc.backend.user_service import UserService

catalogue_service = CatalogueService()
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


@app.route('/catalogue', methods=['POST', 'GET', 'DELETE'])
def add_content():
    ''' Used to add a new module or course to the catalogue
    '''
    request_data = request.get_json()
    service = SERVICE_ROUTER.get(request_data.get('type'))
    if request.method == 'POST':
        institutions = [institution_service.get_by_id_raw(request_data[
            'institution_id'])]
        del(request_data['type'])
        del(request_data['institution_id'])
        result = service.create(**request_data)
        service.add_many_to_many(result, institutions, 'institutions')
        return jsonify({'message': 'data added successfully', 
                        'data': request_data,
                        'status': 200})
    elif request.method == 'DELETE':
        return jsonify(service.soft_delete(request_data['type'],
                            request_data['id'], 
                            request_data['institution_id'], 
                            'institutions'))


@app.route('/catalogue/enrol', methods=['POST', 'DELETE'])
def enrollment():
    '''  Used to enrol a user on a module or course
        :param: content_id - maps to a module or course depending on type param
        :param: type - string - 'module' or 'course' 
    '''
    request_data = request.get_json()
    service = SERVICE_ROUTER.get(request_data.get('type'))
    if request.method == 'POST':
        response = service.enrol(request_data['user_id'], 
            request_data['content_ids'])
        return jsonify({'message': 'data added successfully', 'data': response,
         'status': 200})
    
    elif request.method == 'DELETE':
        for content_id in request_data['content_ids']:
            delete_response = service.soft_delete(request_data['type'],
                            content_id, 
                            request_data['user_id'], 
                            'student') 
            delete_response['message'] = 'You have successfully cancelled your enrollment on the {} {}'.\
            format(delete_response['to_delete'], 
                request_data['type'])
        return jsonify(delete_response)



@app.route('/catalogue/students/<int:id>', methods=['GET'])
def student(id):
    ''' Fetch a users enrollments 
    '''
    return jsonify(user_service.get_by_id(id))










