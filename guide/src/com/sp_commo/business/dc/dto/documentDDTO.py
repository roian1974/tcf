class documentDDTO :
    articleID = ""
    content = ""
    registerDate = ""

    def __init__(self):
        self.articleID = ""
        self.content = ""
        self.registerDate = "99999999"
        print('EArticle 인스턴스 객체가 메모리에서 생성되었습니다.')

    def __init__(self,articleID,content,registerDate):
        self.registerDate = registerDate
        self.articleID = articleID
        self.content = content

    def getDic(self):
        dic = {}
        dic['articleID'] = self.articleID
        dic['content'] = self.content
        dic['registerDate'] = self.registerDate
        return dic

    def getDic2(self):
        dic = {}
        dic['key'] = self.articleID
        dic['values']  = self.articleScore + ',' + self.content + ',' + self.registerDate
        return dic
