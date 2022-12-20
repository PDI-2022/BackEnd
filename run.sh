rm -rf ./instance
rm -rf ./migrations 

export FLASK_APP=app.py
flask db init 
flask db migrate
flask db upgrade
flask seed_default_user
flask seed_default_model
flask create_cortez_and_lucimara

flask run