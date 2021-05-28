from flask import Flask, g
import flask_session
from flask_session import Session
from admin import admin


app = Flask(__name__)
app.secret_key = 'somescretekeythatonlyishouldknow'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.jpeg', '.gif', '.bmp', '.tif']
app.config["IMAGE_UPLOADS"] = "/mnt/c/wsl/projects/pythonise/tutorials/flask_series/app/app/static/img/uploads"


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

ALLOWED_HOSTS = ['*']

app.register_blueprint(
    admin.admin_dp,
    url_prefix='/profile/'
)


from controllers import *


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
    