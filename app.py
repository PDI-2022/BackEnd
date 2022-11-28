from api.routes.process import process_bp
from api.routes.model import model_bp
from api.routes.view import view_bp
from flask_cors import CORS
from config import app
import threading
import sys
import webview

CORS(app,origins=["*"])

app.register_blueprint(process_bp)
app.register_blueprint(model_bp)
app.register_blueprint(view_bp)


def start_server():
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    webview.create_window('TetraSeed - Classificação de Sementes de Feijão', url='http://localhost:5000/',width=800, height=600, \
                      resizable=True, fullscreen=False, \
                      min_size=(1280, 768), hidden=False, frameless=False, \
                      minimized=False, on_top=False, confirm_close=True, \
                      background_color='#FFF', text_select=False)

    webview.start()
    sys.exit()