from flask import request

from webargs import fields
from webargs.flaskparser import use_args

from mightyMooc import app, db
from mightyMooc.backend.catalogue_service import CatalogueService
from mightyMooc.backend.module_service import ModuleService


@app.route('/catalogue')
def catalogue():
    return CatalogueService().get()

module_args = {
    'name': fields.Str(required=False)
}

@use_args(module_args)
@app.route('/module/{name}')
def module(**kwargs):
    return ModuleService().get(kwargs['name'])







