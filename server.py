from api.routes.upload import upload_bp
from api.routes.model import model_bp
from flask_cors import CORS
from config import app

CORS(app,origins=["*"])

app.register_blueprint(upload_bp)
app.register_blueprint(model_bp)

if __name__ == 'main':
  app.run(debug=True)
