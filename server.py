import json

from flask import Flask

from blueprint_owner import owner
from blueprint_platform import platform
from blueprint_user import user

app = Flask(__name__)
app.register_blueprint(owner, url_prefix='/owner')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(platform, url_prefix='/platform')


@app.route('/')
def welcome():
    return json.dumps('Welcome to Rent On')


if __name__ == '__main__':
    app.run(debug=True)
