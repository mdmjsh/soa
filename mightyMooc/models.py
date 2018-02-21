from mightyMooc import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

'''
flask db stamp head - mark all migrations as up to date
'''

class Models():
    def __init__(self):
        self.taxonomy = set()

    def build_taxonomy(self, tablename):
        self.taxonomy.add(tablename)

# wip
def many_to_many_relationship(join_object, parent, child):
    '''
    wip - need to get the primaryjoin |secondaryjoin= lines working 
    as per this example: 

        # exec("row.{} = kwargs['{}']".format(key))

            primaryjoin=(followers.c.follower_id == id),
            secondaryjoin=(followers.c.followed_id == id),

    to be called from the parent table to build a m-m relationship

    :param: join_object - db.table object 
    :param: parent(str) - name of the parent table
    :param: child(str) - name of the child table
    :returns: a many to many relationship to the parent table
    '''
    parent_id = '{}_id'.format(parent[:-1])
    child_id = '{}_id'.format(child[:-1])

    primary_join = ('join_object.c.{}'.format(parent_id))
    secondary_join = ('join_object.c.{}'.format(child_id))
    return db.relationship(
        child, secondary=join_object,
        primaryjoin=('{}==id'.format(eval(primary_join))),
        secondaryjoin=('{}==id'.format(eval(secondary_join))),
    backref=db.backref(parent, lazy='dynamic'), lazy='dynamic')

################ MANY TO MANY RELATIONSHIP OBJECTS ######################
institution_users=db.Table('institution_users',
    db.Column('institution_id', db.Integer, db.ForeignKey('institution.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
        )

module_institutions=db.Table('module_institutions',
    db.Column('module_id', db.Integer, db.ForeignKey('module.id')),
    db.Column('institution_id', db.Integer, db.ForeignKey('institution.id'))
        )

module_tags=db.Table('module_tags',
    db.Column('module_id', db.Integer, db.ForeignKey('module.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
        )

course_modules=db.Table('course_modules',
    db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
    db.Column('module_id', db.Integer, db.ForeignKey('module.id'))
        )

course_institutions=db.Table('course_institutions',
    db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
    db.Column('institution_id', db.Integer, db.ForeignKey('institution.id'))
        )

user_modules=db.Table('user_modules',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('module_id', db.Integer, db.ForeignKey('module.id'))
        )

user_courses=db.Table('user_courses',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
        )

################################################################

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime)
    updated_up = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime)
    last_sign_in = db.Column(db.DateTime)
    user_type = db.Column(db.String(32))
    modules = db.relationship('Module', secondary=user_modules,
        # primaryjoin=(user_modules.c.user_id == id),
        # secondaryjoin=(user_modules.c.module_id == id),
        backref=db.backref('users', lazy='dynamic'), lazy='dynamic')
    courses = db.relationship('Course', secondary=user_courses,
        # primaryjoin=(user_modules.c.user_id == id),
        # secondaryjoin=(user_modules.c.module_id == id),
        backref=db.backref('users', lazy='dynamic'), lazy='dynamic')

    # modules = many_to_many_relationship(user_modules, 'users', 'modules')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Institution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(64), index=True, unique=True)
    created_at = db.Column(db.DateTime)
    updated_up = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime)
    users = db.relationship('User', secondary=institution_users,
        # primaryjoin=(institution_users.c.institution_id == id),
        # secondaryjoin=(institution_users.c.user_id == id),
        backref=db.backref('institutions', lazy='dynamic'), lazy='dynamic')


class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(64), index=True)
    created_at = db.Column(db.DateTime)
    updated_up = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime)
    description = db.Column(db.Text)
    tags = db.relationship('Tag', secondary=module_tags,
        # primaryjoin=(module_categories.c.module_id == id),
        # secondaryjoin=(module_categories.c.category_id == id),
        backref=db.backref('modules', lazy='dynamic'), lazy='dynamic')

    institutions = db.relationship('Institution', secondary=module_institutions,
        # primaryjoin=(module_institutions.c.module_id == id),
        # secondaryjoin=(module_institutions.c.institution_id == id),
        backref=db.backref('modules', lazy='dynamic'), lazy='dynamic')


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(64), index=True, unique=True)
    created_at = db.Column(db.DateTime)
    updated_up = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.Text)
    level = db.Column(db.String(64))
    created_at = db.Column(db.DateTime)
    updated_up = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime)
    institutions = db.relationship('Institution', secondary=course_institutions,
        # primaryjoin=(course_institutions.c.course_id == id),
        # secondaryjoin=(course_institutions.c.institution_id == id),
        backref=db.backref('courses', lazy='dynamic'), lazy='dynamic')

    modules = db.relationship('Module', secondary=course_modules,
        # Commented out as 'sqlalchemy.orm.exc.UnmappedColumnError' on insert
        # primaryjoin=(course_modules.c.course_id == id),  
        # secondaryjoin=(course_modules.c.module_id == id),
        backref=db.backref('courses', lazy='dynamic'), lazy='dynamic')




@login.user_loader
def load_user(id):
    return User.query.get(int(id))

