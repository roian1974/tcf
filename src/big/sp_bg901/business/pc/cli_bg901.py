from pprint import pprint
from src.big.sp_bg901.transfer.big9006cdto import BIG9006CDTO
from src.com.fwk.business.tcf import tcf_sp_bg001


# cdto = BIG9006CDTO()
# print(cdto.getDic())
# cdto.dumpJson()

#-- json 파일을 열어서 호출출 INPUT 정보와 모델의 파라미터를 조정하세요
#-- file에는 호출할 json 파일명칭을 넣어세요
file = "C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\\"+"big9006cdto.json"
_big9006cdto = BIG9006CDTO()
djson = _big9006cdto.loadJson(file)

argv=['tcf_sp_bg001.py', 'sp_bg901', 'BIG9006', djson ]
tcf_sp_bg001.main(argv)



