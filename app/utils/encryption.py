from cryptography.fernet import Fernet
from flask import current_app

def get_fernet():
    key = current_app.config['ENCRYPTION_KEY'].strip()
    return Fernet(key.encode())

def encrypt_password(plain_text):
    f = get_fernet()
    return f.encrypt(plain_text.encode()).decode()

def decrypt_password(encrypted_text):
    f = get_fernet()
    return f.decrypt(encrypted_text.encode()).decode()