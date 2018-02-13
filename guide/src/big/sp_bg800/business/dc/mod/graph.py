import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def bar_chart(feature, train):
    sns.set()
    survived = train[train['Survived']==1][feature].value_counts()
    dead = train[train['Survived']==0][feature].value_counts()
    df = pd.DataFrame([survived,dead])
    df.index = ['Survived','Dead']
    df.plot(kind='bar',stacked=True, figsize=(10,5))
    plt.show()


def bar_chart_t2(feature1,feature2,train):
    Pclass1 = train[train[feature1] == 1][feature2].value_counts()
    Pclass2 = train[train[feature1] == 2][feature2].value_counts()
    Pclass3 = train[train[feature1] == 3][feature2].value_counts()
    df = pd.DataFrame([Pclass1, Pclass2, Pclass3])
    df.index = ['1st class', '2nd class', '3rd class']
    df.plot(kind='bar', stacked=True, figsize=(10, 5))
    plt.show()

def face_grid(feature,train) :
    facet = sns.FacetGrid(train, hue="Survived", aspect=4)
    facet.map(sns.kdeplot, feature, shade=True)
    facet.set(xlim=(0, train[feature].max()))
    facet.add_legend()
    plt.show()

    # 특정 부분 확대
    # plt.xlim(0, 20)
