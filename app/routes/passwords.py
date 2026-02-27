from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.password_entry import PasswordEntry
from app.utils.encryption import encrypt_password, decrypt_password
from app.utils.audit import log_action

passwords_bp = Blueprint('passwords', __name__)

# CREATE
@passwords_bp.route('/', methods=['POST'])
@jwt_required()
def create_password():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    if not data or not all(k in data for k in ('site_name', 'site_username', 'password')):
        return jsonify({'error': 'site_name, site_username and password are required'}), 400

    new_entry = PasswordEntry(
        user_id=current_user_id,
        site_name=data['site_name'],
        site_username=data['site_username'],
        encrypted_password=encrypt_password(data['password'])
    )

    db.session.add(new_entry)
    db.session.commit()

    log_action(current_user_id, 'CREATE', new_entry.id)

    return jsonify({'message': 'Password entry created successfully', 'id': new_entry.id}), 201

# READ ALL
@passwords_bp.route('/', methods=['GET'])
@jwt_required()
def get_passwords():
    current_user_id = get_jwt_identity()
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    pagination = PasswordEntry.query.filter_by(user_id=current_user_id).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    log_action(current_user_id, 'READ_ALL')

    return jsonify({
        'entries': [{
            'id': e.id,
            'site_name': e.site_name,
            'site_username': e.site_username,
            'password': decrypt_password(e.encrypted_password),
            'created_at': e.created_at.isoformat(),
            'updated_at': e.updated_at.isoformat()
        } for e in pagination.items],
        'pagination': {
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    }), 200

# READ ONE
@passwords_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_password(id):
    current_user_id = get_jwt_identity()
    entry = PasswordEntry.query.filter_by(id=id, user_id=current_user_id).first()

    if not entry:
        return jsonify({'error': 'Entry not found'}), 404
    
    log_action(current_user_id, 'READ', entry.id)

    return jsonify({
        'id': entry.id,
        'site_name': entry.site_name,
        'site_username': entry.site_username,
        'password': decrypt_password(entry.encrypted_password),
        'created_at': entry.created_at.isoformat(),
        'updated_at': entry.updated_at.isoformat()
    }), 200

# UPDATE
@passwords_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_password(id):
    current_user_id = get_jwt_identity()
    entry = PasswordEntry.query.filter_by(id=id, user_id=current_user_id).first()

    if not entry:
        return jsonify({'error': 'Entry not found'}), 404

    data = request.get_json()

    if 'site_name' in data:
        entry.site_name = data['site_name']
    if 'site_username' in data:
        entry.site_username = data['site_username']
    if 'password' in data:
        entry.encrypted_password = encrypt_password(data['password'])

    db.session.commit()

    log_action(current_user_id, 'UPDATE', entry.id)

    return jsonify({'message': 'Entry updated successfully'}), 200

# DELETE
@passwords_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_password(id):
    current_user_id = get_jwt_identity()
    entry = PasswordEntry.query.filter_by(id=id, user_id=current_user_id).first()

    if not entry:
        return jsonify({'error': 'Entry not found'}), 404

    db.session.delete(entry)
    db.session.commit()

    log_action(current_user_id, 'DELETE', entry.id)

    return jsonify({'message': 'Entry deleted successfully'}), 200