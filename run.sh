export FLASK_APP=server.py

rm -rf ./instance
rm -rf ./migrations 

flask db init 
flask db migrate
flask db upgrade

flask run