from flask import Blueprint, request, jsonify
from flask_limiter import Limiter
from miknassa.models import *
from miknassa import bcrypt



apiBp = Blueprint('api', __name__)
limiter = Limiter(apiBp)

@apiBp.route('/users', methods=['POST'])
@limiter.limit('5 per minute', key_func=lambda: request.remote_addr)
def loginUser():
    data = request.json 
    email = data.get('email')
    password = data.get('password')
    
    if email is None or password is None:
        return jsonify({'error': 'Missing email or password'}), 400
    
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return jsonify({'email': user.email, 'password': user.password}), 200
    
    return jsonify({'error': 'User not found'}), 404



# def get_users():
#     users = User.query.all()
#     user_list = []
#     for user in users:
#         user_list.append({'email': user.email, 'password': user.password})
#     return jsonify(user_list), 200