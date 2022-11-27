from api.routes.process import process_bp
from api.routes.model import model_bp
from api.routes.view import view_bp
from flask_cors import CORS
from config import app

CORS(app,origins=["*"])

app.register_blueprint(process_bp)
app.register_blueprint(model_bp)
app.register_blueprint(view_bp)

if __name__ == 'main':
  app.run(debug=True)
