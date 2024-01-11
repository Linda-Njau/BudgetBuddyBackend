from ..models import User
from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token

auth = Blueprint('auth', __name__)

@auth.route('/login',  methods=['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    if not username or not password:
        return jsonify({"msg": "Bad request, missing parameters"}), 400
    user = User.query.filter_by(username=username).first()
    
    if user is None or not user.check_password(password):
        return jsonify({"msg": "Bad username or password"}), 401
    
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token, user_id=user.user_id), 200
    