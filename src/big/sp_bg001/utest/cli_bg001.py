from src.com.fwk.business.tcf import tcf_sp_bg001
from src.big.sp_bg001.transfer.big1000cdto import BIG1000CDTO

"""
    XOR 예측에 대한 모델링
        
"""

cdto = BIG1000CDTO
# 훈련데이타
indata = [
    [0,0],
    [1,0],
    [0,1],
    [1,1]
]
# 훈련데이타 값
labels = [0,1,1,0]

# 테스트데이타
examples = [
    [0,0],
    [1,0]
]
# 테스트데이타값
examples_labels= [0,1]

cdto.indata['indata'] = indata
cdto.indata['labels'] = labels
cdto.indata['examples'] = examples
cdto.indata['examples_labels'] = examples_labels
cdto.indata['domain_function'] = "xorPredict"

argv=['tcf_sp_bg001.py', 'sp_bg001', 'BIG1000', cdto ]
s_out = tcf_sp_bg001.main(argv)

cdto = s_out['outdata'][0]
print('정확도:',cdto.outdata['accuracy'])
print('결과:',cdto.outdata['results'])

