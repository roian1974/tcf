import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.info import include
from src.big.sp_bg004.business.dc.mod import model, features
from src.big.sp_bg004.transfer import big4000cdto

def preAnalysis(big4000cdto) :
    try:
        rtn = True
        # todo: trainning 데이타를 읽는다.

        file = big4000cdto.indata['path'] + big4000cdto.indata['trainfile']
        train = pd.read_csv( file )

        # todo: Data Dictionary 분석
        # • Survived: 0 = No, 1 = Yes
        # • pclass: Ticket  class 1 = 1st, 2 = 2nd, 3 = 3rd        #
        # • sibsp:  # of siblings / spouses aboard the Titanic
        # • parch:  # of parents / children aboard the Titanic
        # • ticket: Ticket number
        # • cabin: Cabin number
        # • embarked: Port of Embarkation C = Cherbourg, Q = Queenstown, S = Southampton

        # todo: 데이타중에서 null 데이타 있는지 확인한다.
        nullData = train.isnull().sum()

        big4000cdto.ddto['trainpd'] = train

    except Exception as err:
        comlogging.logger.error('▲preAnalysis()-ERR:'+ str(err))
        include.setErr('EBIG005', 'preAnalysis 분석에러' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲preAnalysis()-성공:')
    finally:
        if rtn == True :
            return big4000cdto
        else :
            return False


def analysisFeature(big4000cdto) :
    try:
        rtn = True
        # todo : Feature engineering
        # Feature engineering is the process of using domain knowledge of the data
        # to create features (feature vectors) that make machine learning algorithms work.
        # todo: how titanic sank ?
        # sank from the bow of the ship where third class rooms located
        # conclusion, Pclass is key feature for classifier
        # 즉 타이타닉호는 선두가 빙하에 부딪치면서 앞쪽에서 부터 가라앉았다.
        # 이것을 가지고 feature를 분석해보면
        # 3등칸에 탄 손님은 죽을 확률이 높아진다는 특징을 찾아낼수 있다.
        # PassengerId Survived Pclass Name Sex Age SibSp Parch Ticket Fare Cabin Embarked
        # todo-1: 이름의 정보를 통한 특징 찾기

        type = big4000cdto.indata['feature_type']
        if type == "Name" :
            features.getFeatureWithName(big4000cdto)
        elif type == "Sex" :
            features.getFeatureWithSex(big4000cdto)
        elif type == "Age":
            features.getFeatureWithAge(big4000cdto)
        elif type == "Binning":
            features.getFeatureWithBinning(big4000cdto)
        elif type == "Fare":
            features.getFeatureWithFare(big4000cdto)
        elif type == "Cabin":
            features.getFeatureWithCabin(big4000cdto)
        elif type == "Familysize":
            features.getFeatureWithFamilysize(big4000cdto)

    except Exception as err:
        comlogging.logger.error('▲analysisFeature()-ERR:'+ str(err))
        include.setErr('EBIG005', 'analysisFeature 수행 에러' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲analysisFeature()-성공:')
    finally:
        if rtn == True :
            return True
        else :
            return False


def visualModel(big4000cdto) :
    try:
        # modelType = 'Sex', ('Pclass')('SibSp')('Parch')('Embarked')

        graph.bar_chart(big4000cdto.charttype, big4000cdto.trainpd)

    except Exception as err:
        comlogging.logger.error('▲visualModel()-ERR:'+ str(err))
        include.setErr('EBIG005', 'visualModel 수행 에러' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲visualModel()-성공:')
    finally:
        if rtn == True :
            return True
        else :
            return False
