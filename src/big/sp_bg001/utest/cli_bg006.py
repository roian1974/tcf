from src.big.sp_bg001.transfer.big1000cdto import BIG1000CDTO
from src.com.fwk.business.tcf import tcf_sp_bg001

servicename='sp_bg001'
hostprog='BIG1003'
userid='user01'
tpfq=200
cdto = BIG1000CDTO(servicename,hostprog,userid,tpfq)
cdto.indata['arg'] = '100'
cdto.ddto['arg'] = 10

argv=['tcf_sp_bg001.py', servicename, hostprog, cdto ]
tcf_sp_bg001.main(argv)

