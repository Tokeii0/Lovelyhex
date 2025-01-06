import base64
from .base_plugin import BasePlugin

class Base64EncodePlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "Base64编码"
    
    @property
    def description(self) -> str:
        return "将选中的数据进行Base64编码"
    
    def process(self, data: bytes) -> bytes:
        return base64.b64encode(data)

class Base64DecodePlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "Base64解码"
    
    @property
    def description(self) -> str:
        return "将选中的Base64数据解码"
    
    def process(self, data: bytes) -> bytes:
        try:
            return base64.b64decode(data)
        except Exception as e:
            raise ValueError("无效的Base64数据") from e
