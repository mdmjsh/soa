import mightMooc.models, db

class User(object):
	username = ''
    email =''
    password_hash = ''
    created_at = ''
    updated_up = ''
    user_type = ''

    def create(username, email):
    	models.User(username=form.username.data, email=form.email.data)
    	db.session.add(user)
		db.session.commit()
    

    def existing_user():



