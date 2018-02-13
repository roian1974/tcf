import json
import os
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as Features
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, SentimentOptions

def gang() :
    natural_language_understanding = NaturalLanguageUnderstandingV1(
      username="7277ebee-4334-4b09-a3a1-b106566f8cf5",
      password="IgF0ItTeTXnO",
      version="2017-02-27")

    # {
    #   "url": "https://gateway.watsonplatform.net/natural-language-understanding/api",
    #   "username": "7277ebee-4334-4b09-a3a1-b106566f8cf5",
    #   "password": "IgF0ItTeTXnO"
    # }
    #
    # {
    #     "url": "https://gateway.watsonplatform.net/natural-language-understanding/api",
    #     "username": "f842a62b-e902-4cd4-a443-239e49976f59",
    #     "password": "nDGL7hG4zQaO"
    # }

    #f1 = open('C:\\Users\\05455\\Documents\\NLU-PRAC2\\기사1.txt','rt')   # 파일 오픈
    #doc = f1.read()                                                      # 파일내용 읽기


    doc='asdfjflsjalfjlasjlj'
    response = natural_language_understanding.analyze(
        text = doc,
        features=[
            Features.Sentiment(
                  targets=[]
                    )
                 ]
           )
    print(json.dumps(response, indent=2))                                # NLU 결과출력
    #print(response['sentiment']['document']['label'],':', response['sentiment']['document']['score'],'\n')   #

def site() :
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        username="f842a62b-e902-4cd4-a443-239e49976f59",
        password="nDGL7hG4zQaO",
        version="2017-02-27")

    response = natural_language_understanding.analyze(
        url='www.wsj.com/news/markets',
        features=Features(
            sentiment=SentimentOptions(
                targets=[])))


    print(json.dumps(response, indent=2))

site()
