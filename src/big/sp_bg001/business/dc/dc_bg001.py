from src.big.sp_bg001.transfer import bg1000cdto
from sklearn import svm, metrics

def xorPredit(bg1000cdto):
    clf = svm.SVC()
    clf.fit(bg1000cdto.indata, bg1000cdto.labels)
    results = clf.predict(bg1000cdto.examples)
    score = metrics.accuracy_score(bg1000cdto.examples_labels, results)
    print(results)
    print('정확도:', score)


def flowerPredit(bg1000cdto):
    clf = svm.SVC()

    clf.fit(bg1000cdto.indata, bg1000cdto.labels)
    results = clf.predict(bg1000cdto.examples)
    # score = metrics.accuracy_score(bg1000cdto.examples_labels, results)
    print("붓꽃의품종은 ",results)
    # print('정확도:', score)

def flowerPredit2(bg1000cdto):

    clf = svm.SVC()

    clf.fit(bg1000cdto.train_data, bg1000cdto.train_label)

    results = clf.predict(bg1000cdto.test_data)
    score = metrics.accuracy_score(bg1000cdto.test_label,results)

    print("붓꽃의품종은 ",results)
    print('정확도:', score)

