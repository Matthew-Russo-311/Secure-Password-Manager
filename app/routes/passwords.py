from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.password_entry import PasswordEntry

passwords_bp = Blueprint('passwords', __name__)

@passwords_bp.route('/', methods=['GET'])
@jwt_required()
def get_passwords():
    current_user_id = get_jwt_identity()
    return jsonify({'message': f'Hello user {current_user_id}'}), 200