from src.big.sp_bg001.transfer.big1000cdto import BIG1000CDTO
from src.com.fwk.business.tcf import tcf_sp_bg001

servicename='sp_bg001'
hostprog='BIG1005'
userid='user01'
tpfq=200
cdto = BIG1000CDTO(servicename,hostprog,userid,tpfq)
cdto.indata['domain_function'] = "kerasBMI"

argv=['tcf_sp_bg001.py', servicename, hostprog, cdto ]
s_out = tcf_sp_bg001.main(argv)

cdto = s_out['outdata'][0]
print('accuracy',cdto.outdata['accuracy'])
print('loss', cdto.outdata['loss'])