class docsentiment :

    articleID = ""
    articleScore = ""
    label = ""
    modelID = ""
    useYN = ""
    registerDate = ""
    modifyDate = ""

    def __init__(self):
        self.articleID = ""
        self.articleScore = ""
        self.label = ""
        self.useYN = ""
        self.modelID = ""
        self.modifyDate = "99999999"
        self.registerDate = "99999999"
        print('ESentiment 인스턴스 객체가 메모리에서 생성되었습니다.')

    def __init__(self,articleID,label,registerDate,articleScore,modelID,modifyDate,useYN):
        self.registerDate = registerDate
        self.articleID = articleID
        self.label = label
        self.modifyDate = modifyDate
        self.articleScore = articleScore
        self.useYN = useYN
        self.modelID = modelID

    def __del__(self):
       print('ESentiment 인스턴스 객체가 메모리에서 제거됩니다')

    def getDic(self):
        dic = {}
        dic['registerDate'] = self.registerDate
        dic['articleID'] = self.articleID
        dic['label'] = self.label
        dic['modifyDate'] = self.modifyDate
        dic['articleScore'] = self.articleScore
        dic['useYN'] = self.useYN
        dic['modelID'] = self.modelID

        return dic

    def getDic2(self):
        dic = {}
        dic['key'] = self.articleID
        dic['values']  = self.articleScore + ',' + self.label + ',' + self.modelID + self.registerDate
        return dic
