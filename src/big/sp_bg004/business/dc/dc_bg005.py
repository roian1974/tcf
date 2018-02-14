import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.info import include
from src.big.sp_bg004.business.dc.mod import model, features
from src.big.sp_bg004.transfer import big4000cdto


# -----------------------------------------------------------------------------------------------------------------------
# 개요 :
# 기사내용
# -----------------------------------------------------------------------------------------------------------------------
def preAnalysis(big4000cdto):
    try:
        rtn = True
        # todo: trainning 데이타를 읽는다.
        train = pd.read_csv( big4000cdto.indata['path'] + big4000cdto.indata['trainfile'] )
        test = pd.read_csv(big4000cdto.indata['path'] + big4000cdto.indata['testfile'])

        big4000cdto.ddto['testpd'] = test
        big4000cdto.ddto['trainpd'] = train

        #-name----------------------------------------------------------------------------------------------------------
        train_test_data = [train, test]  # combining train and test dataset
        for dataset in train_test_data:
            dataset['Title'] = dataset['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)

        # print(train['Title'].value_counts())

        title_mapping = {"Mr": 0, "Miss": 1, "Mrs": 2,
                         "Master": 3, "Dr": 3, "Rev": 3, "Col": 3, "Major": 3, "Mlle": 3, "Countess": 3,
                         "Ms": 3, "Lady": 3, "Jonkheer": 3, "Don": 3, "Dona": 3, "Mme": 3, "Capt": 3, "Sir": 3}
        for dataset in train_test_data:
            dataset['Title'] = dataset['Title'].map(title_mapping)

        # print(train.head())
        train.drop('Name', axis=1, inplace=True)
        test.drop('Name', axis=1, inplace=True)
        # print(train.head())
        #-sex--------------------------------------------------------------------------------------------------------------
        sex_mapping = {"male": 0, "female": 1}
        for dataset in train_test_data:
            dataset['Sex'] = dataset['Sex'].map(sex_mapping)

        #-age-------------------------------------------------------------------------------------------------------------
        # fill missing age with median age for each title (Mr, Mrs, Miss, Others)
        train["Age"].fillna(train.groupby("Title")["Age"].transform("median"), inplace=True)
        test["Age"].fillna(test.groupby("Title")["Age"].transform("median"), inplace=True)
        # print(train.groupby("Title")["Age"].transform("median"))

        big4000cdto.ddto['train_data'] = train.drop('Survived', axis=1)
        big4000cdto.ddto['target'] = train['Survived']
        big4000cdto.ddto['test_data'] = test.drop("PassengerId", axis=1).copy()

    except Exception as err:
        comlogging.logger.error('▲preAnalysis()-ERR:' + str(err))
        include.setErr('EBIG005', 'preAnalysis 분석에러' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲preAnalysis()-성공:')
    finally:
        if rtn == True:
            return big4000cdto
        else:
            return False


def trainModel(big4000cdto):
    try:
        rtn = True
        modelType = big4000cdto.indata['model_type']

        if modelType == "KNN":
            model.trainKNN(big4000cdto)

        elif modelType == "DT":
            model.trainDecisionTree(big4000cdto)

        else:
            pass

    except Exception as err:
        comlogging.logger.error('▲trainModel()-ERR:' + str(err))
        include.setErr('EBIG005', 'trainModel 수행 에러' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲trainModel()-성공:')
    finally:
        if rtn == True:
            return True
        else:
            return False


def testModel(big4000cdto):
    try:
        rtn = True
        modelType = big4000cdto.indata['model_type']

        if modelType == "KNN":
            model.testKNN(big4000cdto)
        if modelType == "SVM":
            model.testSVM(big4000cdto)

        else:
            pass

    except Exception as err:
        comlogging.logger.error('▲testModel()-ERR:' + str(err))
        include.setErr('EBIG005', 'testModel 수행 에러' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲testModel()-성공:')
    finally:
        if rtn == True:
            return True
        else:
            return False


