import pandas as pd

raw_data = {'regiment': ['Nighthawks', 'Nighthawks', 'Nighthawks', 'Nighthawks', 'Dragoons', 'Dragoons', 'Dragoons', 'Dragoons', 'Scouts', 'Scouts', 'Scouts', 'Scouts'],
            'company': ['infantry', 'infantry', 'cavalry', 'cavalry', 'infantry', 'infantry', 'cavalry', 'cavalry','infantry', 'infantry', 'cavalry', 'cavalry'],
            'experience': ['**vet**er22an', 'rookie', 'veteran', 'rookie', 'veteran', 'rookie', 'veteran', 'rookie','veteran', 'rookie', 'veteran', 'rookie'],
            'name': ['Miller', 'Jacobson', 'Ali', 'Milner', 'Cooze', 'Jacon', 'Ryaner', 'Sone', 'Sloan', 'Piger', 'Riani', 'Ali'],
            'preTestScore': [4, 24, 31, 2, 3, 4, 24, 31, 2, 3, 2, 3],
            'postTestScore': [25, 94, 57, 62, 70, 25, 94, 57, 62, 70, 62, 70]
            }

df = pd.DataFrame(raw_data, columns = ['regiment', 'company', 'experience', 'name', 'preTestScore', 'postTestScore'])
print(df)
print("------------------------------------------------------------------------------------------------------")

# 2x2 테이블
# regiment를 기준으로 하여 company의 빈도를 구한다.
data = pd.crosstab(df.regiment, df.company, margins=True)
print(data)


slicedData = df.iloc[:, 2:4]  # tail.iloc[ 행, 열]
slicedData.replace(to_replace="[^a-zA-Z]", value=" ", regex=True, inplace=True)
print("-----------")
print(slicedData)


