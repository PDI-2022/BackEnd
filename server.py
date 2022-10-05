from flask import Flask
from api.upload import upload_bp
from flask_cors import CORS


app = Flask(__name__)
CORS(app,origins=["*"])

app.register_blueprint(upload_bp)
if __name__ == "__main__":
  app.run()