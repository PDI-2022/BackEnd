from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
import click
from api.constants.folders import models_folder
import os

template_dir = os.path.abspath("./views")
static_dir = os.path.abspath("./static")

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@click.command(name="seed_default_model")
@with_appcontext
def seed_default_model():
    from db.models import Model

    model_name = "inception9"
    default_model = db.session.query(Model).filter_by(name=model_name).first()
    if default_model is None:
        path_to_model = "{0}/{1}".format(models_folder, model_name)
        default_model = Model(name=model_name, path=path_to_model)
        db.session.add(default_model)
        db.session.commit()


@click.command(name="seed_default_user")
@with_appcontext
def seed_default_user():
    from db.models import User

    user_email = "usuario_admin@alu.ufc.br"
    default_user = db.session.query(User).filter_by(email=user_email).first()
    if default_user is None:
        default_user = User(user_email, "12345678")
        db.session.add(default_user)
        db.session.commit()


app.cli.add_command(seed_default_model)
app.cli.add_command(seed_default_user)
