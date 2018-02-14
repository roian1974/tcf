import urllib.request as req

# 1단계 : 소스파일을 다운로드 받는다.
#-----------------------------------------------------------------------------------------------------------------------
# local= "./mushroom/mushroom.csv"
# url = "https://archive.ics.uci.edu/ml/machine-learning-databases/mushroom/agaricus-lepiota.data"
# req.urlretrieve(url, local)
# print("ok")

# p,x,s,n,t,p,f,c,n,k,e,e,s,s,w,w,p,w,o,p,k,s,u - p 로시작하면 독이 있는 버섯 - 레이블
# e,x,s,y,t,a,f,c,b,k,e,c,s,s,w,w,p,w,o,p,n,n,g - e 이면 먹을수 있는 버섯 - 레이블

#  ord 함수는 알파벳을 숫자로 바꾸어주는 함수

from src.big.sp_bg001.transfer.big1000cdto import BIG1000CDTO
from src.com.fwk.business.tcf import tcf_sp_bg001
from src.com.fwk.business.info import include

servicename='sp_bg001'
hostprog='BIG1004'
userid='user01'
tpfq=200
cdto = BIG1000CDTO(servicename,hostprog,userid,tpfq)
cdto.indata['model_type'] = "Randomforest"
cdto.indata['file'] = './mushroom/mushroom.csv'

argv=['tcf_sp_bg001.py', servicename, hostprog, cdto ]
s_out = tcf_sp_bg001.main(argv)

cdto = s_out['outdata'][0]
print(cdto.outdata['accuracy'])
print(cdto.outdata['report'])



