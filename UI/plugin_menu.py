from PySide6.QtWidgets import QMenu, QMessageBox
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction
from plugins.plugin_manager import PluginManager

class PluginMenu(QMenu):
    pluginTriggered = Signal(object, bytes)  # 插件, 数据
    
    def __init__(self, parent=None):
        super().__init__("插件", parent)
        self.plugin_manager = PluginManager()
        self.setup_menu()
    
    def setup_menu(self):
        """设置插件菜单"""
        self.clear()
        for plugin in self.plugin_manager.get_plugins():
            action = QAction(plugin.name, self)
            action.setToolTip(plugin.description)
            action.setData(plugin)
            action.triggered.connect(lambda checked, p=plugin: self.on_plugin_triggered(p))
            self.addAction(action)
    
    def on_plugin_triggered(self, plugin):
        """处理插件触发事件"""
        if hasattr(self.parent(), 'get_selected_data'):
            data = self.parent().get_selected_data()
            if data:
                try:
                    result = self.plugin_manager.process_data(plugin, data)
                    if result is not None:
                        self.pluginTriggered.emit(plugin, result)
                except Exception as e:
                    QMessageBox.warning(self, "错误", str(e))
