import os
from datetime import datetime

class FileManager:
    @staticmethod
    def get_file_info(file_path: str):
        """获取文件信息"""
        try:
            stat = os.stat(file_path)
            return {
                'size': stat.st_size,
                'created_time': datetime.fromtimestamp(stat.st_ctime),
                'modified_time': datetime.fromtimestamp(stat.st_mtime),
                'accessed_time': datetime.fromtimestamp(stat.st_atime)
            }
        except Exception as e:
            print(f"获取文件信息失败: {str(e)}")
            return None
    
    @staticmethod
    def read_file_chunk(file_path: str, offset: int, chunk_size: int = 1024 * 1024):
        """分块读取文件内容"""
        try:
            with open(file_path, 'rb') as f:
                f.seek(offset)
                return f.read(chunk_size)
        except Exception as e:
            print(f"读取文件块失败: {str(e)}")
            return None
    
    @staticmethod
    def write_file_chunk(file_path: str, offset: int, data: bytes):
        """写入文件块"""
        try:
            with open(file_path, 'r+b') as f:
                f.seek(offset)
                f.write(data)
                return True
        except Exception as e:
            print(f"写入文件块失败: {str(e)}")
            return False
