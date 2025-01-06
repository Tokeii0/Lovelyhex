from abc import ABC, abstractmethod

class BasePlugin(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """插件名称"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """插件描述"""
        pass
    
    @abstractmethod
    def process(self, data: bytes) -> bytes:
        """处理数据"""
        pass
    
    @property
    def input_type(self) -> str:
        """输入数据类型，可以是 'text' 或 'hex'"""
        return 'text'  # 默认为文本类型
    
    @property
    def output_type(self) -> str:
        """输出数据类型，可以是 'text' 或 'hex'"""
        return 'text'  # 默认为文本类型
