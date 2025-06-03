import os
from config import Config
import logging

logger = logging.getLogger(__name__)

def handle_large_upload(file_id, chunk_index, chunk_file):
    """处理分片上传"""
    chunk_dir = os.path.join(Config.UPLOAD_FOLDER, 'chunks', file_id)
    os.makedirs(chunk_dir, exist_ok=True)
    
    chunk_path = os.path.join(chunk_dir, f'{chunk_index:05d}')
    try:
        chunk_file.save(chunk_path)
        logger.info(f"Chunk {chunk_index} for file {file_id} saved successfully")
        return True
    except Exception as e:
        logger.error(f"Error saving chunk {chunk_index} for file {file_id}: {str(e)}")
        return False

def merge_uploaded_chunks(file_id, filename):
    """合并分片为完整文件"""
    # 验证文件类型
    if not allowed_file(filename):
        logger.error(f"Invalid file type: {filename}")
        return False
    
    chunk_dir = os.path.join(Config.UPLOAD_FOLDER, 'chunks', file_id)
    
    # 检查分片目录是否存在
    if not os.path.exists(chunk_dir):
        logger.error(f"Chunk directory not found for file {file_id}")
        return False
    
    chunks = sorted(os.listdir(chunk_dir))
    if not chunks:
        logger.error(f"No chunks found for file {file_id}")
        return False
    
    final_path = os.path.join(Config.UPLOAD_FOLDER, filename)
    
    try:
        # 合并文件
        with open(final_path, 'wb') as outfile:
            for chunk in chunks:
                chunk_path = os.path.join(chunk_dir, chunk)
                with open(chunk_path, 'rb') as infile:
                    outfile.write(infile.read())
        
        logger.info(f"File {filename} merged successfully from {len(chunks)} chunks")
        
        return True
    except Exception as e:
        logger.error(f"Error merging chunks for file {filename}: {str(e)}")
        return False
    finally:
        # 清理分片
        try:
            for chunk in chunks:
                os.remove(os.path.join(chunk_dir, chunk))
            os.rmdir(chunk_dir)
        except Exception as e:
            logger.warning(f"Error cleaning up chunks: {str(e)}")

def allowed_file(filename):
    """文件类型白名单"""
    if '.' not in filename:
        return False
    
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in Config.ALLOWED_EXTENSIONS