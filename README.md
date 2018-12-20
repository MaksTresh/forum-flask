# forum-flask
## Getting Started
Change absolute paths

*config.py*
```
#line 5
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(r'your\path\forum-flask\app', 'app.db')
```
*app\routes.py*
```
#line 5
UPLOAD_FOLDER = r'your\path\forum-flask\uploads'
```
## Run
```
cd your\path\forum-flask\
$ venv\Scripts\activate
(venv) $ flask run
```
