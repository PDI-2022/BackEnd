from flask import Blueprint, render_template, request
from config import app
import requests

view_bp = Blueprint('view', __name__)

@app.route("/", methods=['GET'])
def index():
    try:
        models = requests.get("http://localhost:5000/api/v1/models")
        modelJson = models.json()
    except:
        modelJson = [{"name":"","id":""}]
    return render_template("index.html",models=modelJson)

@app.route("/seeds", methods=['GET'])
def seeds():
    print(request.get_data())
    return render_template("seeds.html")

@app.route("/uploadModel", methods=['GET'])
def model():
    return render_template("uploadModel.html")

@app.route("/login", methods=['GET'])
def login():
    return render_template("login.html")

@app.route("/new-user", methods=['GET'])
def novoUsuario():
    return render_template("novoUsuario.html")

@app.route("/forgot-password", methods=['GET'])
def novaSenha():
    return render_template("novaSenha.html")