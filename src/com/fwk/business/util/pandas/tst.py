# cluster org time
# 1   a   8
# 1   a   6
# 2   h   34
# 1   c   23
# 2   d   74
# 3   w   6

import pandas as pd
data = pd.DataFrame({"cluster" : [1,1,2,1,2,3], "org":['a','a','h','c','d','w'], "time":[8,6,34,23, 74,6]})
print(data)

data = data.sort_values(["time"], ascending=[False])
print(data)

data = data.reset_index(drop=True)
print(data)

slicedData = data.iloc[:, 2:27]  # tail.iloc[ 행, 열]
slicedData.replace(to_replace="[^a-zA-Z]", value=" ", regex=True, inplace=True)
print(slicedData)




