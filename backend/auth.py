import os
import hmac
import jwt
import time
from functools import wraps
from flask import request, jsonify, g

API_KEY = os.environ.get('API_SECRET_KEY', 'default-api-key')
JWT_SECRET = os.environ.get('JWT_SECRET', 'jwt-super-secret')

def constant_time_compare(val1, val2):
    """安全比较字符串（避免时序攻击）"""
    return hmac.compare_digest(str(val1), str(val2))

def api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        provided_key = request.headers.get('X-API-Key')
        if not provided_key or not constant_time_compare(provided_key, API_KEY):
            return jsonify({
                'error': 'Unauthorized',
                'message': '无效的API密钥'
            }), 401
        return f(*args, **kwargs)
    return decorated_function

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({
                'error': 'Unauthorized',
                'message': '缺少认证Token'
            }), 401
        
        try:
            token = token[7:]  # 去掉 "Bearer "
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            g.current_user = payload['sub']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token已过期'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': '无效Token'}), 401
        
        return f(*args, **kwargs)
    return decorated_function

def generate_token(username):
    payload = {
        'sub': username,
        'iat': int(time.time()),
        'exp': int(time.time()) + 3600 * 24  # 1天有效期
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')