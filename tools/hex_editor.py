class HexEditor:
    def __init__(self):
        self.data = bytearray()
        self.file_path = None
    
    def load_file(self, file_path: str):
        """加载文件内容"""
        try:
            with open(file_path, 'rb') as f:
                self.data = bytearray(f.read())
            self.file_path = file_path
            return True
        except Exception as e:
            print(f"加载文件失败: {str(e)}")
            return False
    
    def save_file(self, file_path: str = None):
        """保存文件内容"""
        if file_path is None:
            file_path = self.file_path
        
        if file_path is None:
            return False
        
        try:
            with open(file_path, 'wb') as f:
                f.write(self.data)
            return True
        except Exception as e:
            print(f"保存文件失败: {str(e)}")
            return False
    
    def edit_byte(self, offset: int, value: int):
        """编辑指定位置的字节"""
        if 0 <= offset < len(self.data):
            self.data[offset] = value
            return True
        return False
    
    def insert_byte(self, offset: int, value: int):
        """在指定位置插入字节"""
        if 0 <= offset <= len(self.data):
            self.data.insert(offset, value)
            return True
        return False
    
    def delete_byte(self, offset: int):
        """删除指定位置的字节"""
        if 0 <= offset < len(self.data):
            del self.data[offset]
            return True
        return False
    
    def get_size(self):
        """获取数据大小"""
        return len(self.data)
    
    def get_data(self):
        """获取所有数据"""
        return bytes(self.data)
