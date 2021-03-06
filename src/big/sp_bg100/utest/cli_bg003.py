from src.com.fwk.business.tcf import tcf_sp_bg001
from src.big.sp_bg001.transfer import bg1000cdto
import pandas as pd
from sklearn.model_selection import train_test_split

indto = bg1000cdto

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
data = csv[ ["SepalLength","SepalWidth","PetalLength","PetalWidth"] ]
label = csv["Name"]

train_data, test_data , train_label, test_label = train_test_split(data, label)
indto.train_data = train_data
indto.train_label = train_label
indto.test_data = test_data
indto.test_label = test_label
indto.domain_function = "flowerPredit2"

argv=['tcf_sp_bg001.py', 'sp_bg001', 'BIG1000', indto ]
tcf_sp_bg001.main(argv)
