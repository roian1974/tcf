from src.com.fwk.business.util.common import comutil

class BIG9002CDTO :
    keyID = ""
    content = ""
    registerDate = ""
    indata = list()
    outdata = list()

    def __init__(self):
        self.keyID = ""
        self.content = ""
        self.registerDate = comutil.getsysdate()

    def setInit(self,keyID,content,registerDate):
        self.registerDate = registerDate
        self.keyID = keyID
        self.content = content

    def setIndata(self,content) :
        self.indata.append(content)

    def setOutdata(self,content) :
        self.outdata.append(content)

    def getDic(self):
        dic = {}
        dic['keyID'] = self.keyID
        dic['content'] = self.content
        dic['registerDate'] = self.registerDate
        dic['indata'] = self.indata
        dic['outdata'] = self.outdata
        return dic





