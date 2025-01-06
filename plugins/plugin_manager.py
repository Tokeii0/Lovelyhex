import os
import importlib.util
from typing import List, Type
from .base_plugin import BasePlugin

class PluginManager:
    def __init__(self):
        self.plugins = []
        self._load_builtin_plugins()
        self._load_custom_plugins()
    
    def _load_builtin_plugins(self):
        """加载内置插件"""
        from .base64_plugin import Base64EncodePlugin, Base64DecodePlugin
        self.plugins.extend([
            Base64EncodePlugin(),
            Base64DecodePlugin()
        ])
    
    def _load_custom_plugins(self):
        """加载自定义插件"""
        custom_plugin_dir = os.path.join(os.path.dirname(__file__), 'custom')
        if not os.path.exists(custom_plugin_dir):
            os.makedirs(custom_plugin_dir)
        
        for file in os.listdir(custom_plugin_dir):
            if file.endswith('.py') and not file.startswith('_'):
                try:
                    plugin_path = os.path.join(custom_plugin_dir, file)
                    spec = importlib.util.spec_from_file_location(
                        f"custom_plugin_{file[:-3]}", 
                        plugin_path
                    )
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        
                        # 查找模块中的插件类
                        for attr_name in dir(module):
                            attr = getattr(module, attr_name)
                            if (isinstance(attr, type) and 
                                issubclass(attr, BasePlugin) and 
                                attr != BasePlugin):
                                self.plugins.append(attr())
                except Exception as e:
                    print(f"加载插件 {file} 失败: {str(e)}")
    
    def get_plugins(self) -> List[BasePlugin]:
        """获取所有插件"""
        return self.plugins
    
    def process_data(self, plugin: BasePlugin, data: bytes) -> bytes:
        """使用插件处理数据"""
        try:
            return plugin.process(data)
        except Exception as e:
            raise ValueError(f"插件处理失败: {str(e)}")
    
    @staticmethod
    def create_plugin_template(plugin_name: str) -> str:
        """创建插件模板"""
        return f'''from plugins.base_plugin import BasePlugin

class {plugin_name}Plugin(BasePlugin):
    @property
    def name(self) -> str:
        return "{plugin_name}"
    
    @property
    def description(self) -> str:
        return "插件描述"
    
    def process(self, data: bytes) -> bytes:
        # 在这里实现你的数据处理逻辑
        return data
'''
