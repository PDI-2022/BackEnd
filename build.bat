@REM Gerando os arquivos para deploy em /dist
pyinstaller -n "tetraseed" --icon ".\static\Assets\Logo\logo.ico" --onefile --clean --add-data "db;db" --add-data "api;api" --add-data "static;static" --add-data "migrations;migrations" --add-data "models;models" --add-data "views;views" --hidden-import "flask_api.parsers" --hidden-import "flask_api.renderers" app.py

