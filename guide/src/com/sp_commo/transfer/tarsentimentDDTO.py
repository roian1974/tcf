class tarsentiment:

    articleID = ""
    target = ""
    targetScore = ""
    label = ""
    useYN = ""
    registerDate = ""
    modifyDate = ""

    def __init__(self):
        self.articleID = ""
        self.targetScore = ""
        self.label = ""
        self.useYN = ""
        self.target = ""
        self.modifyDate = "99999999"
        self.registerDate = "99999999"
        print('ETSentiment 인스턴스 객체가 메모리에서 생성되었습니다.')

    def __init__(self,articleID,label,registerDate,targetScore,modifyDate,useYN,target):
        self.registerDate = registerDate
        self.articleID = articleID
        self.label = label
        self.modifyDate = modifyDate
        self.targetScore = targetScore
        self.useYN = useYN
        self.target = target

    def __del__(self):
       print('ETSentiment 인스턴스 객체가 메모리에서 제거됩니다')

    def getDic(self):
        dic = {}
        dic['registerDate'] = self.registerDate
        dic['articleID'] = self.articleID
        dic['label'] = self.label
        dic['modifyDate'] = self.modifyDate
        dic['targetScore'] = self.targetScore
        dic['useYN'] = self.useYN
        dic['target'] = self.target

    def getDic2(self):
        dic = {}
        dic['key'] = self.articleID + '-' + self.target
        dic['values']  = self.targetScore + ',' + self.label + ',' + self.registerDate
        return dic


