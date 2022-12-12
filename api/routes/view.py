from flask import Blueprint, render_template, request,jsonify
from config import app
import requests
from flask_api import status
from api.services.token import validate
from api.response.error import Error

view_bp = Blueprint('view', __name__)

@app.route("/", methods=['GET'])
def index():
    data,_,role = auth()
    if(data != ""):
        return render_template("login.html")
    try:
        models = requests.get("http://localhost:5000/api/v1/models")
        modelJson = models.json()
    except:
        modelJson = [{"name":"","id":""}]
    return render_template("index.html",models=modelJson,role=role)

@app.route("/seeds", methods=['GET'])
def seeds():
    data,_,role = auth()
    if(data != ""):
        return render_template("login.html")
    return render_template("seeds.html",role=role)

@app.route("/uploadModel", methods=['GET'])
def model():
    data,_,role = auth()
    if(data != "" or role != "ADMIN"):
        return render_template("login.html")
    return render_template("uploadModel.html",role=role)

@app.route("/modelList", methods=['GET'])
def modelList():
    data,_,role = auth()
    if(data != "" or role != "ADMIN"):
        return render_template("login.html")
    return render_template("modelList.html",role=role)

@app.route("/login", methods=['GET'])
def login():
    return render_template("login.html")

@app.route("/new-user", methods=['GET'])
def novoUsuario():
    data,_,role = auth()
    if(data != "" or role != "ADMIN"):
        return render_template("login.html")
    return render_template("novoUsuario.html")

@app.route("/userList", methods=['GET'])
def userList():
    data,_,role = auth()
    if(data != "" or role != "ADMIN"):
        return render_template("login.html")
    return render_template("userList.html",role=role)

@app.route("/forgot-password", methods=['GET'])
def novaSenha():
    return render_template("novaSenha.html")

def auth():
    token = request.cookies.get("token")
    if token is None or token == "":
        return (
            jsonify(
                Error(
                    "O campo token é obrigatório", status.HTTP_400_BAD_REQUEST
                ).__dict__
            ),
            status.HTTP_400_BAD_REQUEST,""
        )
    valid,role = validate(token)
    if not valid:
        return (
            jsonify(
                Error("Usuário não encontrado", status.HTTP_401_UNAUTHORIZED).__dict__
            ),
            status.HTTP_401_UNAUTHORIZED,""
        )

    return "", status.HTTP_200_OK,role
