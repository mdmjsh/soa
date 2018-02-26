import ipdb

from flask import Flask, current_app

from mightyMooc import app, db
from mightyMooc.backend.user_service import UserService
from mightyMooc.backend.institution_service import InstitutionService
from mightyMooc.backend.module_service import ModuleService
from mightyMooc.backend.course_service import CourseService
from mightyMooc.backend.tag_service import TagService


class RunSeed():
    def __init__(self):
        course_service = CourseService()
        module_service = ModuleService()
        tag_service = TagService()
        users =[{'username': 'John', 'email': 'john@example.com'},
        {'username': 'Clare', 'email': 'clare@example.com'}, 
        {'username': 'Mark', 'email': 'mark@example.com' },
        {'username': 'Nasser', 'email': 'nasser@example.com'},
        {'username': 'Fiona', 'email': 'fiona@example.com'}]
        self.generate(users, UserService, 'User')

        institutions =[{'name': 'Oxford'},
        {'name': 'Cambridge'},  
        {'name': 'Imperial',},
        {'name': 'Cardiff'},
        {'name': 'Bristol'}]
        self.generate(institutions, InstitutionService, 'Institution')

        courses =[{'name': 'Programming Fundamentals', 'description': 'An introduction to programming.'},
        {'name': 'Programming for Data Science', 'description': 'Covers some of the mathmatical and programmatic principles required for by modern data science.'}]
        self.generate(courses, CourseService, 'Course')


        p_course_id = CourseService().get_raw(**{'name':'Programming Fundamentals'})[0].id
        ds_course_id = CourseService().get_raw(**{'name':'Programming for Data Science'})[0].id

        prog_modules =[{'name': 'OOP'},
        {'name': 'UI/UX Design'},   
        {'name': 'Databases'},
        {'name': 'Understanding Data structures'},
        {'name': 'Memory Optimization'},
        {'name': 'Testing and debugging'}]
        prog_ids = [i for i in range(1,7)]


        data_science_modules =[
        {'name': 'Statistical Modelling'},
        {'name': 'Probabilistic Graphical Models'},
        {'name': 'Advanced data analytics with Python'},    
        {'name': 'Natural Language Processing'},
        {'name': 'Timeseries Analysis with Spark'},
        {'name': 'Machine Learning'}]
        ds_ids = [i for i in range(8,13)] + [3,4] # Databases and data structures

        modules = prog_modules + data_science_modules   
        self.generate(modules, ModuleService, 'Module')


################### M-2-M course_modules ######################################
        prog_course = course_service.get_raw(**{'name':'Programming Fundamentals'})[0]
        for module_id in prog_ids:
            module = module_service.get_by_id_raw(module_id)
            prog_course.modules.append(module)  
        
        ds_course = course_service.get_raw(**{'name':'Programming for Data Science'})[0]
        for module_id in ds_ids:
            module = module_service.get_by_id_raw(module_id)
            ds_course.modules.append(module) 

################### M-2-M course_institutions ######################################

        oxford = InstitutionService().get_raw(**{'name':'Oxford'})[0]
        cambridge = InstitutionService().get_raw(**{'name':'Cambridge'})[0]
        imperial = InstitutionService().get_raw(**{'name':'Imperial'})[0]
        cardiff = InstitutionService().get_raw(**{'name':'Cardiff'})[0]
        bristol = InstitutionService().get_raw(**{'name':'Bristol'})[0]

        prog_institutions = [oxford, imperial, cardiff]
        ds_institutions = [oxford, cambridge, bristol]

        for institution in prog_institutions:
            institution.courses.append(prog_course) 

        for institution in ds_institutions:
            institution.courses.append(ds_course)



################### M-2-M module_tags ######################################

        # Tags
        programming = tag_service.create(**{'name': 'Programming'})
        python = tag_service.create(**{'name': 'python'})
        sql = tag_service.create(**{'name': 'SQL'})
        rdbms =  tag_service.create(**{'name': 'Relational Database Management Systems'})
        frontend = tag_service.create(**{'name': 'frontend'})
        nodejs = tag_service.create(**{'name': 'node.js'})
        js = tag_service.create(**{'name': 'javaScript'})
        react = tag_service.create(**{'name': 'react'})
        stats = tag_service.create(**{'name': 'Statistics'})
        prob = tag_service.create(**{'name': 'Probabality'})
        analytics = tag_service.create(**{'name': 'Data analytics'})
        nlp = tag_service.create(**{'name': 'NLP'})
        spark = tag_service.create(**{'name': 'Spark'})
        big_data = tag_service.create(**{'name': 'Big data technologies'})

        # Modules 
        oop = module_service.get_raw(**{'name':'OOP'})[0]
        ui = module_service.get_raw(**{'name': 'UI/UX Design'})[0] 
        dbs = module_service.get_raw(**{'name': 'Databases'})[0]
        data_struct = module_service.get_raw(**{
            'name': 'Understanding Data structures'})[0]
        memory = module_service.get_raw(**{'name': 'Memory Optimization'})[0]
        testing = module_service.get_raw(**{'name': 'Testing and debugging'})[0]

        stats_mod = module_service.get_raw(**{'name': 'Statistical Modelling'})[0]
        prob_mod = module_service.get_raw(**{'name': 'Probabilistic Graphical Models'})[0]
        analytics_mod = module_service.get_raw(
            **{'name': 'Advanced data analytics with Python'})[0]
        nlp_mod = module_service.get_raw(**{'name': 'Natural Language Processing'})[0]
        timeseries = module_service.get_raw(
            **{'name': 'Timeseries Analysis with Spark'})[0]
        ml = module_service.get_raw(**{'name': 'Machine Learning'})[0]

        # Build M-2-M tags
        oop.tags.append(programming)
        ui.tags.append(js)
        ui.tags.append(nodejs)
        ui.tags.append(react)
        ui.tags.append(frontend)
        dbs.tags.append(sql)
        dbs.tags.append(rdbms)
        memory.tags.append(programming)
        testing.tags.append(programming)

        data_struct.tags.append(programming)
        stats_mod.tags.append(stats)
        prob_mod.tags.append(prob)
        analytics_mod.tags.append(python)
        analytics_mod.tags.append(programming)
        analytics_mod.tags.append(analytics)
        nlp_mod.tags.append(nlp)
        nlp_mod.tags.append(python)
        timeseries.tags.append(spark)
        timeseries.tags.append(big_data)
        ml.tags.append(big_data)
        ml.tags.append(python)


################### M-2-M module_institutions ################################

        oop.institutions.append(oxford)
        oop.institutions.append(imperial)
        dbs.institutions.append(oxford)
        ui.institutions.append(cardiff)
        memory.institutions.append(imperial)
        testing.institutions.append(oxford)
        data_struct.institutions.append(oxford)
        data_struct.institutions.append(cambridge)
        stats_mod.institutions.append(bristol)
        prob_mod.institutions.append(cambridge)
        analytics_mod.institutions.append(bristol)
        nlp_mod.institutions.append(cambridge)
        timeseries.institutions.append(oxford)
        ml.institutions.append(oxford)


        db.session.commit()


    @staticmethod
    def generate(data, import_object, model):
        create = 'create'
        for row in data:
            getattr(import_object(), create)(**row)
                

if __name__ == "__main__":
    print('Running Seed')
    RunSeed()
    print('Done')

