from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser
from PySide6.QtCore import Qt
import markdown
import markdown.extensions.fenced_code
import markdown.extensions.tables

class MarkdownViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建文本浏览器
        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(True)
        self.layout.addWidget(self.browser)
        
        # 设置样式
        self.browser.setStyleSheet("""
            QTextBrowser {
                background-color: white;
                color: black;
                border: 1px solid #ccc;
                padding: 10px;
            }
        """)
        
        # 添加默认CSS样式
        self.css = """
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; }
                h1, h2, h3 { color: #333; }
                code { background-color: #f5f5f5; padding: 2px 4px; border-radius: 4px; }
                pre { background-color: #f5f5f5; padding: 10px; border-radius: 4px; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f5f5f5; }
                blockquote { border-left: 4px solid #ccc; margin: 0; padding-left: 16px; }
            </style>
        """
    
    def set_markdown(self, text):
        """设置并渲染Markdown内容"""
        # 配置Markdown扩展
        extensions = [
            'fenced_code',
            'tables',
            'nl2br',
            'attr_list'
        ]
        
        # 转换Markdown为HTML
        html = markdown.markdown(text, extensions=extensions)
        
        # 组合完整的HTML文档
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            {self.css}
        </head>
        <body>
            {html}
        </body>
        </html>
        """
        
        # 设置HTML内容
        self.browser.setHtml(full_html)
