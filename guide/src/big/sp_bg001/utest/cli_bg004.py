from src.com.fwk.business.tcf import tcf_sp_bg001
from src.big.sp_bg001.transfer import bg1000cdto
import pandas as pd
from sklearn.model_selection import train_test_split


indto = bg1000cdto

# 손글씨 다운로드
# indto.domain_function = "miniDownload"
# argv=['tcf_sp_bg001.py', 'sp_bg001', 'BIG1000', indto ]
# tcf_sp_bg001.main(argv)

# # 다운로드한 파일을 csv 파일로 저장
# indto = bg1000cdto
# indto.domain_function = "toCSV"
# indto.maxdata = 1000
# indto.file_name = "train"
# argv=['tcf_sp_bg001.py', 'sp_bg001', 'BIG1000', indto ]
# tcf_sp_bg001.main(argv)
# indto.maxdata = 500
# indto.file_name = "t10k"
# argv=['tcf_sp_bg001.py', 'sp_bg001', 'BIG1000', indto ]
# tcf_sp_bg001.main(argv)


# input = "5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,18,18,18,126,136,175,26,166,255,247,127,0,0,0,0,0,0,0,0,0,0,0,0,30,36,94,154,170,253,253,253,253,253,225,172,253,242,195,64,0,0,0,0,0,0,0,0,0,0,0,49,238,253,253,253,253,253,253,253,253,251,93,82,82,56,39,0,0,0,0,0,0,0,0,0,0,0,0,18,219,253,253,253,253,253,198,182,247,241,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,80,156,107,253,253,205,11,0,43,154,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,1,154,253,90,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,139,253,190,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11,190,253,70,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,35,241,225,160,108,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,81,240,253,253,119,25,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,45,186,253,253,150,27,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,93,252,253,187,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,249,253,249,64,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,46,130,183,253,253,207,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,39,148,229,253,253,253,250,182,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,24,114,221,253,253,253,253,201,78,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,23,66,213,253,253,253,253,198,81,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,18,171,219,253,253,253,253,195,80,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,55,172,226,253,253,253,253,244,133,11,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,136,253,253,253,212,135,132,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
# input = input.split(",")
# for i in range(len(input)) :
#     # 3이라고 준 이유는 256처럼 세개의 숫자가 있어 그렇게 준것
#     print("{:3}".format(input[i]), end=" ")
#     if i % 28 == 0:
#         print()

# 훈련데이타
train_csv = pd.read_csv('./mnist/train.csv', header=None)
tk_csv = pd.read_csv('./mnist/t10k.csv', header=None)

# 그런데 데이타는 0과 1사이에서 정하므로
def toDigit(l):
    output = []
    for i in l:
        output.append(float(i)/256)
    return output

indto.train_data = list( map(toDigit, train_csv.iloc[:,1:].values) )
indto.train_label = train_csv[0].values
indto.test_data = list( map(toDigit, tk_csv.iloc[:,1:].values) )
indto.test_label = tk_csv[0].values
indto.domain_function = "handTypeModel"
argv=['tcf_sp_bg001.py', 'sp_bg001', 'BIG1000', indto ]
tcf_sp_bg001.main(argv)