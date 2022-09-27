from flask import Flask
from api.upload import upload_bp

app = Flask(__name__)

app.register_blueprint(upload_bp)

if __name__ == "__main__":
  app.run()