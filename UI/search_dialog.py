from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                                 QLabel, QLineEdit, QPushButton, QCheckBox,
                                 QRadioButton, QButtonGroup, QGroupBox,
                                 QListWidget, QListWidgetItem)
from PySide6.QtCore import Qt, Signal

class SearchDialog(QDialog):
    searchRequested = Signal(str, bool, bool)  # 搜索文本, 是否区分大小写, 是否十六进制搜索
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("查找")
        self.resize(400, 500)
        self.setup_ui()
        self.results = []
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # 搜索输入区域
        search_layout = QHBoxLayout()
        search_label = QLabel("查找内容:")
        self.search_input = QLineEdit()
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # 搜索选项
        options_group = QGroupBox("搜索选项")
        options_layout = QVBoxLayout()
        
        self.case_sensitive = QCheckBox("区分大小写")
        self.hex_search = QCheckBox("十六进制搜索")
        
        options_layout.addWidget(self.case_sensitive)
        options_layout.addWidget(self.hex_search)
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # 搜索结果列表
        results_group = QGroupBox("搜索结果")
        results_layout = QVBoxLayout()
        self.results_list = QListWidget()
        self.results_list.itemDoubleClicked.connect(self.on_result_double_clicked)
        results_layout.addWidget(self.results_list)
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        self.search_button = QPushButton("查找")
        self.search_button.clicked.connect(self.on_search)
        self.close_button = QPushButton("关闭")
        self.close_button.clicked.connect(self.close)
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.close_button)
        layout.addLayout(button_layout)
        
        # 设置回车键触发搜索
        self.search_input.returnPressed.connect(self.on_search)
    
    def on_search(self):
        search_text = self.search_input.text()
        if search_text:
            self.searchRequested.emit(
                search_text,
                self.case_sensitive.isChecked(),
                self.hex_search.isChecked()
            )
    
    def clear_results(self):
        self.results_list.clear()
        self.results = []
    
    def add_result(self, offset, preview):
        """添加搜索结果"""
        self.results.append(offset)
        item = QListWidgetItem(f"偏移: 0x{offset:08X} - {preview}")
        self.results_list.addItem(item)
    
    def on_result_double_clicked(self, item):
        """双击结果项时触发"""
        row = self.results_list.row(item)
        if 0 <= row < len(self.results):
            offset = self.results[row]
            # 通知父窗口跳转到指定位置
            if self.parent():
                self.parent().jump_to_offset(offset)
