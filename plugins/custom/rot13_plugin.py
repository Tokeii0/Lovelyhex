from plugins.base_plugin import BasePlugin
import codecs

class ROT13Plugin(BasePlugin):
    @property
    def name(self) -> str:
        return "ROT13编码/解码"
    
    @property
    def description(self) -> str:
        return "对文本进行ROT13编码或解码"
    
    def process(self, data: bytes) -> bytes:
        # 将bytes解码为文本
        text = data.decode('utf-8')
        # 应用ROT13编码
        result = codecs.encode(text, 'rot_13')
        # 返回编码后的bytes
        return result.encode('utf-8')
