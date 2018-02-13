from googletrans import Translator
# pip install googletrans

# lst = ['The quick brown fox', 'jumps over', 'the lazy dog']
# totype = 'en'
def googletransate(lst,totype) :
    translator = Translator()

    targets = []
    translations = translator.translate(lst, dest=totype)
    for translation in translations:
        print(translation.origin)
        print(translation.text)
        targets.append(translation.text)

lst = [
        u'[아시아경제 박연미 기자] 5일 4대강 사업 입찰 담합 혐의로 1115억원을 웃도는 과징금을 물게된 건설사들은 공정거래위원회의 결정에 강력히 반발했다.   각종 담합을 주도한 인물로 지목된 전(前) A건설 전무는 담합 사실을 전면 부인하면서 "30년 건설밥을 먹었고 15년을 현장소장으로 지내며 야전에서 나라의 기틀을 닦는데 기여했는데 이제와 이런 대접을 받으니 허탈할 따름"이라고 말했다.  B건설사 관계자도 "공정위의 심사보고서는 증거도 논리도 엉성하기 짝이 없다"면서 불복 의사를 분명히 했다.  C건설도 "공정위의 징계에 4대강 사업 특성이 반영되지 않았고, 담합했다는 명시적인 증거가 부족하다"고 반발했다.',
        u'[아시아경제 박연미 기자] 5일 4대강 사업 입찰 담합 혐의로 1115억원을 웃도는 과징금을 물게된 건설사들은 공정거래위원회의 결정에 강력히 반발했다.   각종 담합을 주도한 인물로 지목된 전(前) A건설 전무는 담합 사실을 전면 부인하면서 "30년 건설밥을 먹었고 15년을 현장소장으로 지내며 야전에서 나라의 기틀을 닦는데 기여했는데 이제와 이런 대접을 받으니 허탈할 따름"이라고 말했다.  B건설사 관계자도 "공정위의 심사보고서는 증거도 논리도 엉성하기 짝이 없다"면서 불복 의사를 분명히 했다.  C건설도 "공정위의 징계에 4대강 사업 특성이 반영되지 않았고, 담합했다는 명시적인 증거가 부족하다"고 반발했다.'
       ]

googletransate(lst,'en')

