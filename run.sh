rm -rf ./instance
rm -rf ./migrations 


export FLASK_APP=app.py
flask db init 
flask db migrate
flask db upgrade
flask seed

flask run