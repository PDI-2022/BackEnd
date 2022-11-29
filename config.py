from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
import click 
from api.constants.folders import models_folder
import os
import sys

template_dir = os.path.abspath('./views')
static_dir = os.path.abspath('./static')

if getattr(sys, 'frozen', False):
    template_dir = os.path.join(sys._MEIPASS, 'views')
    static_dir = os.path.join(sys._MEIPASS, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@click.command(name='seed')
@with_appcontext
def seed():
    from db.models import Model
    
    model_name = 'inception4'
    default_model = db.session.query(Model).filter_by(name=model_name).first()
    if default_model is None:
        path_to_model = "{0}/{1}".format(models_folder, model_name)
        default_model = Model(
            name = model_name,
            path = path_to_model
        )
        db.session.add(default_model)
        db.session.commit()

app.cli.add_command(seed)
