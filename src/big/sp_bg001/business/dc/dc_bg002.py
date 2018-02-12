import pandas as pd
import numpy as np
from src.com.fwk.business.util.logging import comlogging
from gensim.models import word2vec
import codecs
from bs4 import BeautifulSoup
from konlpy.tag import Twitter

import matplotlib.pyplot as plt
import seaborn as sns

def word2vecTest() :

    fp = codecs.open('2BEXXX01.txt','r', encoding='utf-8')
    soup = BeautifulSoup(fp, "html.parser")
    body = soup.select_one("text body")
    text = body.getText()

    twitter = Twitter()
    lines = text.split("\r\n")
    results = []
    for line in lines :
        r = []
        malist = twitter.pos(line, norm=True, stem=True)
        for( word, pumsa ) in malist :
            if not pumsa in  ['Josa','Eomi',"Punctuation"] :
                r.append(word)
        results.append( (" ".join(r)).strip())

    out = ( " ".join(results)).strip()
    print(out)

    data = word2vec.LineSentence("")
    model = word2vec.Word2Vec(data,size=200, window=10, hs=1, min_count=2, sq=1)
    model.save("aaa.mod")
