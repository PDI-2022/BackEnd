from api.routes.process import process_bp
from api.routes.model import model_bp
from api.routes.view import view_bp
from api.routes.user import user_bp
from api.routes.login import login_bp
from api.routes.auth import auth_bp
from api.routes.forgot_password import forgot_password_bp
from flask_cors import CORS
from config import app

CORS(app, origins=["*"])

app.register_blueprint(process_bp)
app.register_blueprint(model_bp)
app.register_blueprint(view_bp)
app.register_blueprint(user_bp)
app.register_blueprint(login_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(forgot_password_bp)
if __name__ == "main":
    app.run(debug=True)
