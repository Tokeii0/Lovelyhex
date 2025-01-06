from PySide6.QtWidgets import (QMainWindow, QMenuBar, QStatusBar, 
                                  QTextEdit, QVBoxLayout, QWidget, 
                                  QFileDialog, QTabWidget, QMessageBox)
from PySide6.QtCore import Qt
from .hex_viewer import HexViewer
from .markdown_viewer import MarkdownViewer
from .search_dialog import SearchDialog
from .encoding_dialog import EncodingDialog
from tools.hex_editor import HexEditor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LovelyHex编辑器")
        self.resize(800, 600)
        
        # 初始化编辑器
        self.hex_editor = HexEditor()
        self.current_encoding = 'utf-8'
        
        # 设置中心部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)
        
        # 创建文本编辑器
        self.text_edit = QTextEdit()
        self.tab_widget.addTab(self.text_edit, "文本视图")
        
        # 创建十六进制视图
        self.hex_viewer = HexViewer()
        self.tab_widget.addTab(self.hex_viewer, "十六进制视图")
        
        # 创建Markdown视图
        self.markdown_viewer = MarkdownViewer()
        self.tab_widget.addTab(self.markdown_viewer, "Markdown视图")
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("就绪")
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件")
        file_menu.addAction("打开", self.open_file)
        file_menu.addAction("保存", self.save_file)
        file_menu.addAction("另存为", self.save_as_file)
        file_menu.addSeparator()
        file_menu.addAction("退出", self.close)
        
        # 编辑菜单
        edit_menu = menubar.addMenu("编辑")
        edit_menu.addAction("撤销", self.text_edit.undo)
        edit_menu.addAction("重做", self.text_edit.redo)
        edit_menu.addSeparator()
        edit_menu.addAction("复制", self.text_edit.copy)
        edit_menu.addAction("粘贴", self.text_edit.paste)
        edit_menu.addAction("剪切", self.text_edit.cut)
        edit_menu.addSeparator()
        edit_menu.addAction("查找", self.show_search_dialog)
        
        # 视图菜单
        view_menu = menubar.addMenu("视图")
        view_menu.addAction("文本视图", lambda: self.tab_widget.setCurrentWidget(self.text_edit))
        view_menu.addAction("十六进制视图", lambda: self.tab_widget.setCurrentWidget(self.hex_viewer))
        view_menu.addAction("Markdown视图", lambda: self.tab_widget.setCurrentWidget(self.markdown_viewer))
        
        # 工具菜单
        tools_menu = menubar.addMenu("工具")
        tools_menu.addAction("选择编码", self.show_encoding_dialog)
    
    def show_encoding_dialog(self):
        """显示编码选择对话框"""
        dialog = EncodingDialog(self)
        if dialog.exec_():
            self.current_encoding = dialog.get_selected_encoding()
            self.statusBar.showMessage(f"当前编码: {self.current_encoding}")
            # 如果有打开的文件，重新加载
            if self.hex_editor.file_path:
                self.reload_file_content()
    
    def reload_file_content(self):
        """重新加载文件内容"""
        try:
            # 更新文本视图
            with open(self.hex_editor.file_path, 'r', encoding=self.current_encoding) as f:
                content = f.read()
                self.text_edit.setText(content)
                # 如果是markdown文件，更新markdown视图
                if self.hex_editor.file_path.lower().endswith(('.md', '.markdown')):
                    self.markdown_viewer.set_markdown(content)
        except UnicodeDecodeError:
            self.text_edit.setText(f"[无法使用 {self.current_encoding} 编码解析文件]")
    
    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "打开文件",
            "",
            "所有文件 (*.*)"
        )
        if file_name:
            try:
                # 加载文件到hex_editor
                if self.hex_editor.load_file(file_name):
                    # 更新十六进制视图
                    self.hex_viewer.set_data(self.hex_editor.get_data())
                    
                    # 尝试以文本方式读取
                    try:
                        with open(file_name, 'r', encoding=self.current_encoding) as f:
                            content = f.read()
                            self.text_edit.setText(content)
                            
                            # 如果是markdown文件，更新markdown视图
                            if file_name.lower().endswith(('.md', '.markdown')):
                                self.markdown_viewer.set_markdown(content)
                                self.tab_widget.setCurrentWidget(self.markdown_viewer)
                            else:
                                self.tab_widget.setCurrentWidget(self.text_edit)
                    except UnicodeDecodeError:
                        self.text_edit.setText(f"[无法使用 {self.current_encoding} 编码解析文件]")
                    
                    self.statusBar.showMessage(f"已打开文件: {file_name}")
                else:
                    self.statusBar.showMessage("打开文件失败")
            except Exception as e:
                self.statusBar.showMessage(f"打开文件失败: {str(e)}")
    
    def save_file(self):
        if self.hex_editor.file_path:
            if self.hex_editor.save_file():
                self.statusBar.showMessage("文件已保存")
            else:
                self.statusBar.showMessage("保存文件失败")
        else:
            self.save_as_file()
    
    def save_as_file(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "另存为",
            "",
            "所有文件 (*.*)"
        )
        if file_name:
            if self.hex_editor.save_file(file_name):
                self.statusBar.showMessage(f"文件已保存为: {file_name}")
            else:
                self.statusBar.showMessage("保存文件失败")

    def show_search_dialog(self):
        """显示搜索对话框"""
        from .search_dialog import SearchDialog
        if not hasattr(self, 'search_dialog'):
            self.search_dialog = SearchDialog(self)
            self.search_dialog.searchRequested.connect(self.perform_search)
        self.search_dialog.show()
        self.search_dialog.raise_()
        self.search_dialog.activateWindow()
    
    def perform_search(self, search_text, case_sensitive, hex_search):
        """执行搜索"""
        self.search_dialog.clear_results()
        
        if hex_search:
            try:
                # 将十六进制字符串转换为bytes
                pattern = bytes.fromhex(search_text.replace(' ', ''))
                results = self.hex_viewer.search_hex(pattern, case_sensitive)
            except ValueError:
                self.statusBar.showMessage("无效的十六进制格式")
                return
        else:
            results = self.hex_viewer.search_text(search_text, case_sensitive)
        
        # 显示结果
        for offset in results:
            preview = self.hex_viewer.get_preview(offset)
            self.search_dialog.add_result(offset, preview)
        
        # 更新状态栏
        self.statusBar.showMessage(f"找到 {len(results)} 个匹配项")
    
    def jump_to_offset(self, offset):
        """跳转到指定偏移位置"""
        self.tab_widget.setCurrentWidget(self.hex_viewer)
        self.hex_viewer.jump_to_offset(offset)
