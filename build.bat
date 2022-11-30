@REM python -m pip install --upgrade pip
@REM pip install -r requirements.txt
@REM subsituir o hook-shapely no env
pyinstaller -n "tetraseed" --icon ".\static\Assets\Logo\logo.ico" --clean --onefile --windowed --add-data "db;db" --add-data "instance;instance" --add-data "api;api" --add-data "static;static" --add-data "migrations;migrations" --add-data "models;models" --add-data "views;views" --hidden-import "flask_api.parsers" --hidden-import "flask_api.renderers"  app.py
@REM --onefile