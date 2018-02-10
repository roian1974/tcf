import pandas as pd
import pickle
import numpy as np
from src.com.fwk.business.util.logging import comlogging
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from src.com.fwk.business.util.common import comutil

def trainKNN(pbig8001cdto) :
    try:
        rtn = True
        train_data = pbig8001cdto.dic['train_data']
        target = pbig8001cdto.dic['target']

        print( train_data.shape, target.shape)

        k_fold = KFold(n_splits=10, shuffle=True, random_state=0)

        clf = KNeighborsClassifier(n_neighbors=13)
        scoring = 'accuracy'
        score = cross_val_score(clf, train_data, target, cv=k_fold, n_jobs=1, scoring=scoring)
        print(score)
        score = round(np.mean(score) * 100, 2)

    except Exception as err:
        rtn = False
        comlogging.logger.error( 'execute' + str(err))
    else:
        comlogging.logger.info( 'execute-성공-')
    finally:
        if rtn == True :
            return score
        else :
            return False


def trainDecisionTree(pbig8001cdto) :
    try:
        rtn = True
        train_data = pbig8001cdto.dic['train_data']
        target = pbig8001cdto.dic['target']

        print( train_data.shape, target.shape)

        k_fold = KFold(n_splits=10, shuffle=True, random_state=0)

        clf = DecisionTreeClassifier()
        scoring = 'accuracy'

        print(k_fold,clf,scoring)
        score = cross_val_score(clf, train_data, target, cv=k_fold, n_jobs=1, scoring=scoring)
        print(score)

        score = round(np.mean(score) * 100, 2)

    except Exception as err:
        rtn = False
        comlogging.logger.error( 'execute' + str(err))
    else:
        comlogging.logger.info( 'execute-성공-')
    finally:
        if rtn == True :
            return score
        else :
            return False

def trainRandomForest(pbig8001cdto) :
    try:
        rtn = True
        train_data = pbig8001cdto.dic['train_data']
        target = pbig8001cdto.dic['target']

        k_fold = KFold(n_splits=10, shuffle=True, random_state=0)

        clf = RandomForestClassifier(n_estimators=13)
        scoring = 'accuracy'
        score = cross_val_score(clf, train_data, target, cv=k_fold, n_jobs=1, scoring=scoring)

        score = round(np.mean(score) * 100, 2)

    except Exception as err:
        rtn = False
        comlogging.logger.error( 'execute' + str(err))
    else:
        comlogging.logger.info( 'execute-성공-')
    finally:
        if rtn == True :
            return score
        else :
            return False

def trainNaiveBayes(pbig8001cdto) :
    try:
        rtn = True
        train_data = pbig8001cdto.dic['train_data']
        target = pbig8001cdto.dic['target']

        k_fold = KFold(n_splits=10, shuffle=True, random_state=0)

        clf = GaussianNB()
        scoring = 'accuracy'
        score = cross_val_score(clf, train_data, target, cv=k_fold, n_jobs=1, scoring=scoring)
        score = round(np.mean(score) * 100, 2)

    except Exception as err:
        rtn = False
        comlogging.logger.error( 'execute' + str(err))
    else:
        comlogging.logger.info( 'execute-성공-')
    finally:
        if rtn == True :
            return score
        else :
            return False


def trainSVM(pbig8001cdto) :
    try:
        rtn = True
        train_data = pbig8001cdto.dic['train_data']
        target = pbig8001cdto.dic['target']

        k_fold = KFold(n_splits=10, shuffle=True, random_state=0)

        clf = SVC()
        scoring = 'accuracy'
        score = cross_val_score(clf, train_data, target, cv=k_fold, n_jobs=1, scoring=scoring)
        print(score)
        score = round(np.mean(score) * 100, 2)

    except Exception as err:
        rtn = False
        comlogging.logger.error( 'execute' + str(err))
    else:
        comlogging.logger.info( 'execute-성공-')
    finally:
        if rtn == True :
            return score
        else :
            return False


def testSVM(pbig8001cdto) :
    try:
        rtn = True
        train_data = pbig8001cdto.dic['train_data']
        target = pbig8001cdto.dic['target']
        test_data = pbig8001cdto.dic['test_data']
        test = pbig8001cdto.testpd

        clf = SVC()
        clf.fit(train_data, target)
        prediction = clf.predict(test_data)

        submission = pd.DataFrame({
            "PassengerId": test["PassengerId"],
            "Survived": prediction
        })

        submission.to_csv('submission.csv', index=False)

        submission = pd.read_csv('submission.csv')
        print( submission.head())


    except Exception as err:
        rtn = False
        comlogging.logger.error( 'execute' + str(err))
    else:
        comlogging.logger.info( 'execute-성공-')
    finally:
        if rtn == True :
            return submission
        else :
            return False
