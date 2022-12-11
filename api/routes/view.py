from flask import Blueprint, render_template, request
from config import app
from api.services.token import extract_role
import requests

view_bp = Blueprint("view", __name__)


@app.route("/", methods=["GET"])
def index():
    role = ""
    token = request.cookies.get("token")
    if token is not None:
        role = extract_role(token)
    try:
        models = requests.get("http://localhost:5000/api/v1/models")
        modelJson = models.json()
    except:
        modelJson = [{"name": "", "id": ""}]
    return render_template("index.html", models=modelJson, role=role)


@app.route("/seeds", methods=["GET"])
def seeds():
    role = ""
    token = request.cookies.get("token")
    if token is not None:
        role = extract_role(token)
    return render_template("seeds.html", role=role)


@app.route("/uploadModel", methods=["GET"])
def model():
    role = ""
    token = request.cookies.get("token")
    if token is not None:
        role = extract_role(token)
    return render_template("uploadModel.html", role=role)


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/new-user", methods=["GET"])
def novoUsuario():
    return render_template("novoUsuario.html")


@app.route("/forgot-password", methods=["GET"])
def novaSenha():
    return render_template("novaSenha.html")
