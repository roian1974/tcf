from src.com.fwk.business.tcf import tcf_sp_bg001
from src.big.sp_bg001.transfer import bg1000cdto

indto = bg1000cdto
# 훈련데이타
indto.indata = [
    [0,0],
    [1,0],
    [0,1],
    [1,1]
]
# 훈련데이타 값
indto.labels = [0,1,1,0]

# 테스트데이타
indto.examples = [
    [0,0],
    [1,0]
]
# 테스트데이타값
indto.examples_labels= [0,1]
indto.domain_function = "xorPredict"

argv=['tcf_sp_bg001.py', 'sp_bg001', 'BIG1000', indto ]
tcf_sp_bg001.main(argv)
