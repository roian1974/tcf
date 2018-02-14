from src.big.sp_bg002.transfer.big2000cdto import BIG2000CDTO
from src.com.fwk.business.tcf import tcf_sp_bg001

servicename='sp_bg002'
hostprog='BIG2000'
userid='user01'
tpfq=200
cdto = BIG2000CDTO(servicename,hostprog,userid,tpfq)

# # ----- cli send data
# cdto.indata['filename'] = "C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\Full_Data.csv"
# cdto.indata['model'] = "LogisR" # [NaiveEyes,RF,SVMGusian,SVMLinear]
# cdto.indata['basedate'] = "20150101"
# cdto.indata['ftype'] = 'EN' # [KO]
# cdto.indata['d_type'] = 'train' # train, test
#
# # ---- call server
# argv=['tcf_sp_bg001.py', servicename, hostprog, cdto ]
# s_out = tcf_sp_bg001.main(argv)
#
# if cdto.indata['d_type'] == "test" :
#     cdto = s_out['outdata'][0]
#     print(cdto.outdata['out'])

# ----- cli send data
cdto.indata['filename'] = "C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\Full_Data.csv"
cdto.indata['model'] = "LogisR" # [NaiveEyes,RF,SVMGusian,SVMLinear]
cdto.indata['basedate'] = "20150101"
cdto.indata['ftype'] = 'EN' # [KO]
cdto.indata['d_type'] = 'test' # train, test

# ---- call server
argv=['tcf_sp_bg001.py', servicename, hostprog, cdto ]
s_out = tcf_sp_bg001.main(argv)

if cdto.indata['d_type'] == "test" :
    cdto = s_out['outdata'][0]
    print(cdto.outdata['out'])
