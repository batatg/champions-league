from webargs.flaskparser import use_args
from flask import Flask
from webargs import fields

from main.utils import query_result_handler, DynamicJSONEncoder
from main.models import db_session
from main.service import create_user


app = Flask(__name__)
app.json_encoder = DynamicJSONEncoder

user_args = {
    # Required arguments
    "first_name": fields.Str(required=True, validate=lambda x: x != ''),
    "last_name": fields.Str(required=True),
    "email": fields.Email(required=True),
    "password": fields.Str(required=True, validate=lambda x: len(x) > 7)
}


@app.route("/api/users/", methods=['GET'])
@query_result_handler()
@use_args(user_args)
def hello(args):
    first_name = args['first_name']
    last_name = args['last_name']
    email = args['email']
    password = args['password']
    return create_user(first_name, last_name, email, password)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(port=8001)