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

def trainKNN(big4000cdto) :
    try:
        rtn = True
        train_data = [ big4000cdto.ddto['train_data'] ]
        target = big4000cdto.ddto['target']

        features_drop = ['Ticket', 'Name', 'PassengerId']
        train_data = train_data.drop(features_drop, axis=1)

        cabin_mapping = {"A": 0, "B": 0.4, "C": 0.8, "D": 1.2, "E": 1.6, "F": 2, "G": 2.4, "T": 2.8}
        for dataset in [train_data]:
            dataset['Cabin'] = dataset['Cabin'].map(cabin_mapping)

        train_data["FamilySize"] = train_data["SibSp"] + train_data["Parch"] + 1


        print( train_data.shape, target.shape)
        print( train_data.info())

        print(train_data.head(10))


        k_fold = KFold(n_splits=10, shuffle=True, random_state=0)

        clf = KNeighborsClassifier(n_neighbors=13)

        scoring = 'accuracy'
        print("----1",scoring)
        score = cross_val_score(clf, train_data, target, cv=k_fold, n_jobs=1, scoring=scoring)
        print('----2')
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


def trainDecisionTree(big4000cdto) :
    try:
        rtn = True
        train_data = big4000cdto.ddto['train_data']
        target = big4000cdto.ddto['target']

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

def trainRandomForest(big4000cdto) :
    try:
        rtn = True
        train_data = big4000cdto.ddto['train_data']
        target = big4000cdto.ddto['target']

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

def trainNaiveBayes(big4000cdto) :
    try:
        rtn = True
        train_data = big4000cdto.ddto['train_data']
        target = big4000cdto.ddto['target']

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


def trainSVM(big4000cdto) :
    try:
        rtn = True
        train_data = big4000cdto.ddto['train_data']
        target = big4000cdto.ddto['target']

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


def testSVM(big4000cdto) :
    try:
        rtn = True
        train_data = big4000cdto.ddto['train_data']
        target = big4000cdto.ddto['target']
        test_data = big4000cdto.ddto['test_data']
        test = big4000cdto.testpd

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
