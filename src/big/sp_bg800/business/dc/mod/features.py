import pandas as pd
import matplotlib.pyplot as plt
from src.com.fwk.business.util.logging import comlogging
from src.big.sp_bg800.business.dc.mod import graph


def getFeatureWithName(pbig8001cdto) :
    try:
        rtn = True
        train_l = [ pbig8001cdto.trainpd ]
        train = pbig8001cdto.trainpd

        for dataset in train_l:
            dataset['Title'] = dataset['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)

        out = train['Title'].value_counts()
        comlogging.logger.info(str(out))

        # 남자 : 0, 결혼안한여자 : 1, 결혼한여자 : 2, 나머지 : 3
        title_mapping = {"Mr": 0, "Miss": 1, "Mrs": 2,
                         "Master": 3, "Dr": 3, "Rev": 3, "Col": 3, "Major": 3, "Mlle": 3, "Countess": 3,
                         "Ms": 3, "Lady": 3, "Jonkheer": 3, "Don": 3, "Dona": 3, "Mme": 3, "Capt": 3, "Sir": 3}
        for dataset in train_l:
            dataset['Title'] = dataset['Title'].map(title_mapping)

        comlogging.logger.info(str(train.head()))

        graph.bar_chart('Title',pbig8001cdto.trainpd)

    except Exception as err:
        rtn = False
        comlogging.logger.error('▲getFeatureWithName()-ERR:' + str(err))
    else:
        pass
    finally:
        if rtn == True :
            return dataset
        else :
            return False


def getFeatureWithSex(pbig8001cdto) :
    try:
        rtn = True
        train_l = [ pbig8001cdto.trainpd ]
        train = pbig8001cdto.trainpd

        sex_mapping = {"male": 0, "female": 1}
        for dataset in train_l:
            dataset['Sex'] = dataset['Sex'].map(sex_mapping)

        comlogging.logger.info(str(train.head()))

        graph.bar_chart('Sex',train )

    except Exception as err:
        rtn = False
        comlogging.logger.error('▲getFeatureWithSex()-ERR:' + str(err))
    else:
        pass
    finally:
        if rtn == True :
            return dataset
        else :
            return False

def getFeatureWithAge(pbig8001cdto) :
    try:
        rtn = True
        train_l = [ pbig8001cdto.trainpd ]
        train = pbig8001cdto.trainpd

        for dataset in train_l:
            dataset['Title'] = dataset['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)

        out = train['Title'].value_counts()
        comlogging.logger.info(str(out))

        # 남자 : 0, 결혼안한여자 : 1, 결혼한여자 : 2, 나머지 : 3
        title_mapping = {"Mr": 0, "Miss": 1, "Mrs": 2,
                         "Master": 3, "Dr": 3, "Rev": 3, "Col": 3, "Major": 3, "Mlle": 3, "Countess": 3,
                         "Ms": 3, "Lady": 3, "Jonkheer": 3, "Don": 3, "Dona": 3, "Mme": 3, "Capt": 3, "Sir": 3}
        for dataset in train_l:
            dataset['Title'] = dataset['Title'].map(title_mapping)

        sex_mapping = {"male": 0, "female": 1}
        for dataset in train_l:
            dataset['Sex'] = dataset['Sex'].map(sex_mapping)

        # delete unnecessary feature from dataset
        train.drop('Name', axis=1, inplace=True)

        # fill missing age with median age for each title (Mr, Mrs, Miss, Others)
        train["Age"].fillna(train.groupby("Title")["Age"].transform("median"), inplace=True)
        out = train.groupby("Title")["Age"].transform("median")
        comlogging.logger.info(str(train))

        graph.face_grid('Age',train)


    except Exception as err:
        rtn = False
        comlogging.logger.error('▲getFeatureWithAge()-ERR:' + str(err))
    else:
        pass
    finally:
        if rtn == True :
            return out
        else :
            return False

def getFeatureWithBinning(pbig8001cdto) :
    try:
        rtn = True
        train_l = [ pbig8001cdto.trainpd ]
        train = pbig8001cdto.trainpd

        # Binning / Converting Numerical Age to Categorical Variable
        # -------------------------------------------------------------------------------------------------------------
        # feature vector map:
        # child: 0
        # young: 1
        # adult: 2
        # mid - age: 3
        # senior: 4

        for dataset in train_l:
            dataset.loc[ dataset['Age'] <= 16, 'Age'] = 0,  # 어린아이
            dataset.loc[(dataset['Age'] > 16) & (dataset['Age'] <= 26), 'Age'] = 1, #청소년
            dataset.loc[(dataset['Age'] > 26) & (dataset['Age'] <= 36), 'Age'] = 2, #어른
            dataset.loc[(dataset['Age'] > 36) & (dataset['Age'] <= 62), 'Age'] = 3, #장년
            dataset.loc[ dataset['Age'] > 62, 'Age'] = 4 #노인

        graph.bar_chart('Age',train)

    except Exception as err:
        rtn = False
        comlogging.logger.error('▲getFeatureWithSex()-ERR:' + str(err))
    else:
        pass
    finally:
        if rtn == True :
            return dataset
        else :
            return False

def getFeatureWithFare(pbig8001cdto) :
    try:
        rtn = True
        train_l = [ pbig8001cdto.trainpd ]
        train = pbig8001cdto.trainpd

        # fill missing Fare with median fare for each Pclass
        train["Fare"].fillna(train.groupby("Pclass")["Fare"].transform("median"), inplace=True)
        # train.head(50)

        graph.face_grid('Fare', train)

    except Exception as err:
        rtn = False
        comlogging.logger.error('▲getFeatureWithSex()-ERR:' + str(err))
    else:
        pass
    finally:
        if rtn == True :
            return pbig8001cdto
        else :
            return False


def getFeatureWithCabin(pbig8001cdto) :
    try:
        rtn = True
        train_l = [ pbig8001cdto.trainpd ]
        train = pbig8001cdto.trainpd


        # train.Cabin.valalus
        out = train.Cabin.value_counts()
        comlogging.logger.info(str(out))

        for dataset in train_l:
            dataset['Cabin'] = dataset['Cabin'].str[:1]

        graph.bar_chart_t2('Pclass','Cabin',train)

    except Exception as err:
        rtn = False
        comlogging.logger.error('▲getFeatureWithSex()-ERR:' + str(err))
    else:
        pass
    finally:
        if rtn == True :
            return pbig8001cdto
        else :
            return False


def getFeatureWithFamilysize(pbig8001cdto):
    try:
        rtn = True
        train_l = [pbig8001cdto.trainpd]
        train = pbig8001cdto.trainpd

        train["FamilySize"] = train["SibSp"] + train["Parch"] + 1

        graph.face_grid("FamilySize",train)

        sex_mapping = {"male": 0, "female": 1}
        for dataset in train_l:
            dataset['Sex'] = dataset['Sex'].map(sex_mapping)

        # delete unnecessary feature from dataset
        train.drop('Name', axis=1, inplace=True)

        family_mapping = {1: 0, 2: 0.4, 3: 0.8, 4: 1.2, 5: 1.6, 6: 2, 7: 2.4, 8: 2.8, 9: 3.2, 10: 3.6, 11: 4}
        for dataset in train_l:
            dataset['FamilySize'] = dataset['FamilySize'].map(family_mapping)

        comlogging.logger.info(str(train.head()))

    except Exception as err:
        rtn = False
        comlogging.logger.error('▲getFeatureWithSex()-ERR:' + str(err))
    else:
        pass
    finally:
        if rtn == True:
            return pbig8001cdto
        else:
            return False
