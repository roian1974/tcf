import urllib.request as req
from src.big.sp_bg004.transfer.big4000cdto import BIG4000CDTO
from src.com.fwk.business.tcf import tcf_sp_bg001
from src.com.fwk.business.info import include

servicename='sp_bg004'
hostprog='BIG4001'
userid='user01'
tpfq=200
cdto = BIG4000CDTO(servicename,hostprog,userid,tpfq)
cdto.indata['trainfile'] = "titanic_train.csv"
cdto.indata['testfile'] = "titanic_test.csv"
cdto.indata['path'] = "C:\jDev\MyWorks\PycharmProjects\Roian\src\\big\sp_bg004\\utest\data\\"
cdto.indata['domain_function'] = "trainModel"
cdto.indata['model_type'] = "KNN" # DT

argv=['tcf_sp_bg001.py', servicename, hostprog, cdto ]
s_out = tcf_sp_bg001.main(argv)

cdto = s_out['outdata'][0]
print(cdto.outdata['accuracy'])
print(cdto.outdata['report'])

