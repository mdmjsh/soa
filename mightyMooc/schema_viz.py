import os
from sqlalchemy import MetaData
from sqlalchemy_schemadisplay import create_schema_graph

def run():
	basedir = os.path.abspath(os.path.dirname(__file__))
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
	        'sqlite:///' + os.path.join(basedir, 'app.db')
	print(SQLALCHEMY_DATABASE_URI)

	# create the pydot graph object by autoloading all tables via a bound metadata object
	graph = create_schema_graph(metadata=MetaData(SQLALCHEMY_DATABASE_URI),
	   show_datatypes=False, # The image would get nasty big if we'd show the datatypes
	   show_indexes=False, # ditto for indexes
	   rankdir='LR', # From left to right (instead of top to bottom)
	   concentrate=False # Don't try to join the relation lines together
	)
	graph.write_png('dbschema.png') # write out the file

if __name__ == '__main__':
	run()