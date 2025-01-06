from PySide6.QtWidgets import (QWidget, QTextEdit, QVBoxLayout, QHBoxLayout,
                               QScrollBar, QMenu, QLabel)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QTextCursor, QTextCharFormat, QColor, QTextBlockFormat
from .plugin_menu import PluginMenu

class HexEdit(QTextEdit):
    """自定义的十六进制编辑器组件"""
    scrolled = Signal(int)  # 发送滚动位置
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setFont(self.get_monospace_font())
        self.setStyleSheet("""
            QTextEdit {
                background-color: white;
                color: black;
                border: 1px solid #ccc;
            }
        """)
        
        # 禁用默认的右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
    
    def get_monospace_font(self):
        font = QFont("Consolas, Courier New")
        font.setStyleHint(QFont.Monospace)
        font.setPointSize(10)
        return font
    
    def wheelEvent(self, event):
        super().wheelEvent(event)
        # 发送滚动位置
        self.scrolled.emit(self.verticalScrollBar().value())

class HexViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
        # 存储当前数据
        self.current_data = None
        self.bytes_per_line = 16
        self.highlight_format = QTextCharFormat()
        self.highlight_format.setBackground(QColor(255, 255, 0, 100))
        
        # 创建插件菜单
        self.plugin_menu = PluginMenu(self)
        self.plugin_menu.pluginTriggered.connect(self.on_plugin_result)
    
    def setup_ui(self):
        """设置UI布局"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 添加标题行
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("偏移"), 1)
        header_layout.addWidget(QLabel("十六进制"), 4)
        header_layout.addWidget(QLabel("ASCII"), 2)
        layout.addLayout(header_layout)
        
        # 创建水平布局来放置两个编辑器
        editor_layout = QHBoxLayout()
        
        # 创建十六进制显示区域
        self.hex_edit = HexEdit()
        self.hex_edit.customContextMenuRequested.connect(self.show_context_menu)
        editor_layout.addWidget(self.hex_edit, 5)  # 分配更多空间给十六进制部分
        
        # 创建ASCII显示区域
        self.ascii_edit = HexEdit()
        self.ascii_edit.customContextMenuRequested.connect(self.show_context_menu)
        editor_layout.addWidget(self.ascii_edit, 2)
        
        layout.addLayout(editor_layout)
        
        # 同步滚动
        self.hex_edit.scrolled.connect(self.sync_scroll_ascii)
        self.ascii_edit.scrolled.connect(self.sync_scroll_hex)
    
    def sync_scroll_hex(self, value):
        """同步十六进制视图的滚动"""
        if self.hex_edit.verticalScrollBar().value() != value:
            self.hex_edit.verticalScrollBar().setValue(value)
    
    def sync_scroll_ascii(self, value):
        """同步ASCII视图的滚动"""
        if self.ascii_edit.verticalScrollBar().value() != value:
            self.ascii_edit.verticalScrollBar().setValue(value)
    
    def format_hex_line(self, offset: int, data: bytes) -> tuple[str, str]:
        """格式化一行十六进制数据，返回(hex_str, ascii_str)"""
        # 十六进制部分
        hex_parts = []
        ascii_parts = []
        
        for i, byte in enumerate(data):
            hex_parts.append(f"{byte:02X}")
            if i > 0 and i % 8 == 7:
                hex_parts.append("")
            
            # ASCII部分
            if 32 <= byte <= 126:
                ascii_parts.append(chr(byte))
            else:
                ascii_parts.append(".")
        
        # 补齐不足16字节的部分
        while len(hex_parts) < 16:
            hex_parts.append("  ")
            ascii_parts.append(" ")
            if len(hex_parts) % 9 == 8:
                hex_parts.append("")
        
        hex_line = f"{offset:08X}  {' '.join(hex_parts)}"
        ascii_line = "".join(ascii_parts)
        
        return hex_line, ascii_line
    
    def set_data(self, data: bytes):
        """显示十六进制数据"""
        self.current_data = data
        if not data:
            self.hex_edit.clear()
            self.ascii_edit.clear()
            return
        
        hex_lines = []
        ascii_lines = []
        
        for offset in range(0, len(data), 16):
            chunk = data[offset:offset + 16]
            hex_line, ascii_line = self.format_hex_line(offset, chunk)
            hex_lines.append(hex_line)
            ascii_lines.append(ascii_line)
        
        self.hex_edit.setText("\n".join(hex_lines))
        self.ascii_edit.setText("\n".join(ascii_lines))
    
    def show_context_menu(self, pos):
        """显示右键菜单"""
        sender = self.sender()
        if sender and sender.textCursor().hasSelection():
            menu = QMenu(self)
            menu.addMenu(self.plugin_menu)
            menu.exec_(sender.mapToGlobal(pos))
    
    def get_selected_data(self) -> bytes:
        """获取选中区域的字节数据"""
        if not self.current_data:
            return b""
        
        # 检查哪个编辑器被选中
        if self.hex_edit.hasFocus() and self.hex_edit.textCursor().hasSelection():
            cursor = self.hex_edit.textCursor()
            selected_text = cursor.selectedText()
            try:
                # 移除所有空格和其他非十六进制字符
                hex_text = "".join(c for c in selected_text if c.isalnum())
                return bytes.fromhex(hex_text)
            except ValueError:
                return b""
        elif self.ascii_edit.hasFocus() and self.ascii_edit.textCursor().hasSelection():
            cursor = self.ascii_edit.textCursor()
            selected_text = cursor.selectedText()
            return selected_text.encode('utf-8')
        
        return b""
    
    def on_plugin_result(self, plugin, result: bytes):
        """处理插件处理结果"""
        # 确定哪个编辑器被选中
        if self.hex_edit.hasFocus():
            cursor = self.hex_edit.textCursor()
            if cursor.hasSelection():
                cursor.insertText(result.hex(' ').upper())
        elif self.ascii_edit.hasFocus():
            cursor = self.ascii_edit.textCursor()
            if cursor.hasSelection():
                try:
                    text_result = result.decode('utf-8')
                    cursor.insertText(text_result)
                except UnicodeDecodeError:
                    pass
        
        # 显示处理结果
        try:
            text_result = result.decode('utf-8')
            self.window().statusBar().showMessage(f"处理结果: {text_result}")
        except UnicodeDecodeError:
            self.window().statusBar().showMessage(f"处理完成: {len(result)} 字节")
