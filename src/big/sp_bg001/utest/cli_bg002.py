from src.com.fwk.business.tcf import tcf_sp_bg001
from src.big.sp_bg001.transfer.big1000cdto import BIG1000CDTO
import pandas as pd


# 훈련데이타 가공
"""
 5.1,3.5,1.4,0.2,Iris-setosa
4.9,3.0,1.4,0.2,Iris-setosa
4.7,3.2,1.3,0.2,Iris-setosa
7.0,3.2,4.7,1.4,Iris-versicolor
6.4,3.2,4.5,1.5,Iris-versicolor
6.9,3.1,4.9,1.5,Iris-versicolor

1) 모델은 숫자만 인식하므로 Iris-setosa-> 0, Iris-versicolor ->1 ...으로 변환한다.
5.1,3.5,1.4,0.2,1
4.9,3.0,1.4,0.2,1
4.7,3.2,1.3,0.2,1
7.0,3.2,4.7,1.4,0
6.4,3.2,4.5,1.5,0
6.9,3.1,4.9,1.5,0

"""
# 훈련데이타
csv = pd.read_csv('./flower/iris2.csv')
train = csv[ ["SepalLength","SepalWidth","PetalLength","PetalWidth"] ]
label = csv["Name"]

cdto = BIG1000CDTO

cdto.indata['indata'] = train
cdto.indata['labels'] = label
cdto.indata['examples'] = [ [5.1, 3.0, 1.3, 0.2] ]
cdto.indata['examples_labels'] = []
cdto.indata['domain_function'] = "flowerPredit"

argv=['tcf_sp_bg001.py', 'sp_bg001', 'BIG1001', cdto ]
s_out = tcf_sp_bg001.main(argv)

cdto = s_out['outdata'][0]
print('정확도:',cdto.outdata['accuracy'])
print('결과:',cdto.outdata['results'])

