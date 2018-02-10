# pip install googletrans

from googletrans import Translator

translator = Translator()
msg = translator.translate('저렴한 가격에 괜찮은 브러시같아요  엉킨 머리카락도 부드럽게 빗어지고요 딱딱하지도 않아서 두피에 자극도 많이 없어서 좋아요 .')
print(msg.text)
print(msg)

# <Translated src=ko dest=en text=Good evening. pronunciation=Good evening.>

print( translator.translate('안녕하세요.', dest='en') )
# <Translated src=ko dest=ja text=こんにちは。 pronunciation=Kon'nichiwa.>
translator.translate('veritas lux mea', src='la')
# <Translated src=la dest=en text=The truth is my light pronunciation=The truth is my light>