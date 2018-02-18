from flask import request, current_app

from webargs import fields
from webargs.flaskparser import use_args

from mightyMooc import app, db
from mightyMooc.backend.catalogue_service import CatalogueService
from mightyMooc.backend.module_service import ModuleService
import ipdb


# @app.route('/catalogue')
# def catalogue():
#     return CatalogueService().get()

# module_args = {
#     'name': fields.Str(required=False)
# }

@app.route('/module')
def module():
	if request.args:
		kwargs = request.args.to_dict()
		return ModuleService().get(**kwargs)
	else: 
		return ModuleService().get()

@app.route('/mightymooc/catalogue/addmodule', methods=['POST'])
def add_module(uuid):
    content = request.json
    print(content['mytext'])
    return jsonify({"uuid":uuid})

# curl -H "Content-Type: application/json" -X POST -d '{"name":"xyz","description":"xyz"}' http://localhost:5000//mightymooc/catalogue/addmodule

# @app.route('/mightymooc/catalogue')
# def catalogue():
# 	if request.args:
# 		kwargs = request.args
# 		return CatalogueService().get(**kwargs)
# 	else: 
# 		return CatalogueService().get()

