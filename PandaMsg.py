# coding:utf-8
__author__ = 'Sun'
class PandaMsg(object):

    def __init__(self,content):
        # inital data format of PandaTv
        self.start = bytearray([0x00, 0x06, 0x00, 0x02, 0x00, len(content)])
        self.content = bytes(content.encode("ISO-8859-1"))
        self.end = bytearray([0x00, 0x06, 0x00, 0x00])


    def getBytes(self):
        return bytes(self.start + self.content + self.end)



if __name__ == "__main__":
    sss = '\u5c0f\u72d0\u72f8\u840c\u840c\u54d2\u5462'
    print sss.decode('unicode_escape')

