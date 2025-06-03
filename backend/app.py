import os
import logging
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from auth import api_key_required, jwt_required, generate_token
from bigfile import handle_large_upload, merge_uploaded_chunks
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# 配置日志
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 创建上传目录
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'chunks'), exist_ok=True)

# 用户登录
@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    # 验证凭据（实际应用中应使用更安全的验证方式）
    if username == app.config['ADMIN_USER'] and password == app.config['ADMIN_PASS']:
        token = generate_token(username)
        app.logger.info(f"User {username} logged in successfully")
        return jsonify({
            'success': True,
            'token': token,
            'message': '登录成功'
        }), 200
    return jsonify({'success': False, 'error': '用户名或密码错误'}), 401

# 大文件上传初始化
@app.route('/api/upload/init', methods=['POST'])
@api_key_required
def init_upload():
    filename = secure_filename(request.json['filename'])
    file_size = request.json['size']
    file_id = os.urandom(16).hex()
    
    # 创建上传目录
    upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'chunks', file_id)
    os.makedirs(upload_dir, exist_ok=True)
    
    return jsonify({
        'file_id': file_id,
        'chunk_size': app.config['CHUNK_SIZE'],
        'chunks': -(-file_size // app.config['CHUNK_SIZE'])  # 向上取整
    })

# 处理文件分片上传
@app.route('/api/upload/chunk', methods=['POST'])
@api_key_required
def upload_chunk():
    file_id = request.form['file_id']
    chunk_index = int(request.form['chunk_index'])
    chunk = request.files['chunk']
    
    # 处理上传的分片
    if not handle_large_upload(file_id, chunk_index, chunk):
        return jsonify({'error': '分片上传失败'}), 500
    
    return jsonify({'success': True, 'message': '分片上传成功'})

# 合并文件分片
@app.route('/api/upload/complete', methods=['POST'])
@api_key_required
def complete_upload():
    file_id = request.json['file_id']
    filename = secure_filename(request.json['filename'])
    
    if not merge_uploaded_chunks(file_id, filename):
        return jsonify({'error': '文件合并失败'}), 500
    
    return jsonify({
        'success': True,
        'filename': filename,
        'url': f'/api/download/{filename}'
    })

# 文件下载
@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_from_directory(
            app.config['UPLOAD_FOLDER'],
            filename,
            as_attachment=True
        )
    except FileNotFoundError:
        return jsonify({'error': '文件不存在'}), 404

# 文件列表
@app.route('/api/files', methods=['GET'])
@jwt_required
def list_files():
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.isfile(filepath):
            files.append({
                'name': filename,
                'size': os.path.getsize(filepath),
                'created': os.path.getctime(filepath),
                'url': f'/api/download/{filename}'
            })
    return jsonify(files)

# 文件删除
@app.route('/api/files/<filename>', methods=['DELETE'])
@jwt_required
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # 安全验证
    if not os.path.exists(file_path):
        return jsonify({'error': '文件不存在'}), 404
    if not os.path.realpath(file_path).startswith(os.path.realpath(app.config['UPLOAD_FOLDER'])):
        return jsonify({'error': '无效文件路径'}), 400
    
    try:
        os.remove(file_path)
        app.logger.info(f"File {filename} deleted successfully")
        return jsonify({'message': f'文件 {filename} 已删除'}), 200
    except Exception as e:
        app.logger.error(f"Error deleting file {filename}: {str(e)}")
        return jsonify({'error': f'删除失败: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)