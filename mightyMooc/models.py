from mightyMooc import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


def many_to_many_relationship(join_object, parent, child):
    '''
    to be called from the parent table to build a m-m relationship

    :param: join_object - db.table object 
    :param: parent(str) - name of the parent table
    :param: child(str) - name of the child table
    :returns: a many to many relationship to the parent table
    '''
    parent_id = '{}_id'.format(parent)
    child_id = '{}_id'.format(child)
    return db.relationship(
        child, secondary=join_object,
        primaryjoin=(join_object.c.parent_id == id),
        secondaryjoin=(join_object.c.child_id == id),
    backref=db.backref(parent, lazy='dynamic'), lazy='dynamic')


################ MANY TO MANY RELATIONSHIP OBJECTS ######################
institution_users=db.Table('institution_users',
    db.Column('institution_id', db.Integer, db.ForeignKey('institution.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
        )

institution_modules=db.Table('institution_modules',
    db.Column('institution_id', db.Integer, db.ForeignKey('institution.id')),
    db.Column('module_id', db.Integer, db.ForeignKey('module.id'))
        )

module_categories=db.Table('module_categories',
    db.Column('module_id', db.Integer, db.ForeignKey('module.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
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
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime)
    updated_up = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime)
    last_sign_in = db.Column(db.DateTime)
    last_sign_in = db.Column(db.DateTime)
    user_type = db.Column(db.String(32))
    modules = many_to_many_relationship(user_modules, 'user', 'module')


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
    
    # institution_users relational table
    users = many_to_many_relationship(institution_users, 'institution', 'user')

    # db.relationship(
    #     'User', secondary=institution_users,
    #     primaryjoin=(institution_users.c.institution_id == id),
    #     secondaryjoin=(institution_users.c.user_id == id),
    # backref=db.backref('institution', lazy='dynamic'), lazy='dynamic')

    # institution_modules relational table
    modules = many_to_many_relationship(institution_modules, 'institution', 'module')

    # modules = db.relationship(
    #     'Module', secondary=institution_modules,
    #     primaryjoin=(institution_modules.c.institution_id == id),
    #     secondaryjoin=(institution_modules.c.module_id == id),
    # backref=db.backref('institution', lazy='dynamic'), lazy='dynamic')


class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(64), index=True, unique=True)
    created_at = db.Column(db.DateTime)
    updated_up = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime)
    categories = many_to_many_relationship(module_categories, 'module', 'category')


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(64), index=True, unique=True)
    created_at = db.Column(db.DateTime)
    updated_up = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(64), index=True, unique=True)
    created_at = db.Column(db.DateTime)
    updated_up = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime)
    institutions = many_to_many_relationship(course_institutions, 'course', 'institution')
    modules= many_to_many_relationship(course_modules, 'course', 'module')



@login.user_loader
def load_user(id):
    return User.query.get(int(id))