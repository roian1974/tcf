import json
from pprint import pprint
from src.com.fwk.business.util.common import comutil


class BIG8001CDTO:
    # input
    trainfile = 'train.csv'
    testfile = 'test.csv'
    model_type = ''
    path = 'C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\\'
    char_type = ''

    # ddto
    trainpd = ''
    testpd = ''
    dic = { 'train_data':'', 'target':'' }


    def __init__(self):
        pass

    def set_trainfile(self, trainfile):
        self.trainfile = trainfile

    def set_charttype(self, charttype):
        self.charttype = charttype

    def set_testfile(self, testfile):
        self.testfile = testfile

    def set_model_type(self, model_type):
        self.model_type = model_type

    def set_trainpd(self, trainpd):
        self.trainpd = trainpd

    def getDic(self):
        dic = {'input': {}, 'params': {}, 'ddto':{}}

        dic['input']['trainfile'] = self.trainfile
        dic['input']['testfile'] = self.testfile
        dic['input']['model_type'] = self.model_type
        dic['input']['charttype'] = self.charttype
        dic['ddto']['trainpd'] = self.trainpd

        return dic

    def setJson(self, file):
        file = "C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\\" + "big8001cdto.json"
        dic = self.loadJson(file)

        self.trainfile = dic['input']['trainfile']
        self.testfile = dic['input']['testfile']
        self.model_type = dic['input']['model_type']

    def getBIG8001CDTO(self, dic):
        self.trainfile = dic['input']['trainfile']
        self.testfile = dic['input']['testfile']
        self.model_type = dic['input']['model_type']

    def dumpJson(self):
        dic = self.getDic()
        with open('C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\\' + "big8001cdto.json", 'w') as fp:
            json.dump(dic, fp)

    def loadJson(self, file):
        # file = "C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\\"+"big8001cdto.json"
        with open(file) as data_file:
            data = json.load(data_file)
        # pprint(data)

        return data




