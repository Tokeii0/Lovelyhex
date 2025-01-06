from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                                 QLabel, QComboBox, QPushButton)
from PySide6.QtCore import Signal

class EncodingDialog(QDialog):
    encodingSelected = Signal(str)  # 发送选中的编码
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("选择编码")
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # 编码选择框
        encoding_layout = QHBoxLayout()
        encoding_label = QLabel("文件编码:")
        self.encoding_combo = QComboBox()
        
        # 添加常用编码
        common_encodings = [
            'utf-8',
            'gbk',
            'gb2312',
            'utf-16',
            'utf-16le',
            'utf-16be',
            'ascii',
            'iso-8859-1',
            'big5',
            'shift-jis'
        ]
        self.encoding_combo.addItems(common_encodings)
        
        encoding_layout.addWidget(encoding_label)
        encoding_layout.addWidget(self.encoding_combo)
        layout.addLayout(encoding_layout)
        
        # 按钮
        button_layout = QHBoxLayout()
        ok_button = QPushButton("确定")
        cancel_button = QPushButton("取消")
        
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
    
    def get_selected_encoding(self):
        """获取选中的编码"""
        return self.encoding_combo.currentText()
