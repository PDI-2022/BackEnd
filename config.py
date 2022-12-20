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

    model_name = "inception13"
    default_model = db.session.query(Model).filter_by(name=model_name).first()
    if default_model is None:
        model_path = "{0}/{1}".format(models_folder, model_name)
        default_model = Model(model_name, model_path, "Modelo default")
        db.session.add(default_model)
        db.session.commit()


@click.command(name="seed_default_user")
@with_appcontext
def seed_default_user():
    from db.models import User

    user_email = "usuario_admin@ufc.br"
    default_user = db.session.query(User).filter_by(email=user_email).first()
    if default_user is None:
        default_user = User(user_email, "Tr3t@s33d", "ADMIN")
        db.session.add(default_user)
        db.session.commit()

@click.command(name="create_cortez_and_lucimara")
@with_appcontext
def create_cortez_and_lucimara():
    from db.models import User

    user_email_cortez = "cortez.paulo@ufc.br"
    cortez_user = db.session.query(User).filter_by(email=user_email_cortez).first()
    if cortez_user is None:
        default_user = User(user_email_cortez, "cor12tez", "ADMIN")
        db.session.add(default_user)
        db.session.commit()

    user_email_lucimara = "venialluci@gmail.com"
    lucimara_user = db.session.query(User).filter_by(email=user_email_lucimara).first()
    if lucimara_user is None:
        default_user = User(user_email_lucimara, "alegria2022", "ADMIN")
        db.session.add(default_user)
        db.session.commit()


app.cli.add_command(seed_default_model)
app.cli.add_command(seed_default_user)
app.cli.add_command(create_cortez_and_lucimara)

