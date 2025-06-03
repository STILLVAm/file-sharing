import os

class Config:
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super-secret-key')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    
    # 文件上传配置
    MAX_FILE_SIZE = int(os.environ.get('MAX_FILE_SIZE', 10 * 1024 * 1024 * 1024))  # 10GB
    CHUNK_SIZE = int(os.environ.get('CHUNK_SIZE', 100 * 1024 * 1024))  # 100MB
    
    # 管理员凭据
    ADMIN_USER = os.environ.get('ADMIN_USER', 'admin')
    ADMIN_PASS = os.environ.get('ADMIN_PASS', 'admin123')
    
    # 允许的文件扩展名
    ALLOWED_EXTENSIONS = {
        'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 
        'zip', 'mp4', 'mov', 'mp3', 'avi', 'mkv', 'xlsx', 'pptx'
    }
    
    # 日志配置
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'app.log')
    
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        """数据库连接URI"""
        return os.environ.get('DATABASE_URI') or 'sqlite:///file_sharing.db'
    
    @property
    def SQLALCHEMY_TRACK_MODIFICATIONS(self):
        return False