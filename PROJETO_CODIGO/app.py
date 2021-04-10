from flask import Flask, g
from admin import admin

app = Flask(__name__)
app.secret_key = 'somescretekeythatonlyishouldknow'

app.register_blueprint(
    admin.admin_dp,
    url_prefix='/profile/'
)

from controllers import *

if __name__ == "__main__":
    app.run(debug=True, host= '0.0.0.0', port='5000')

#Ultima atualização foi hoje!