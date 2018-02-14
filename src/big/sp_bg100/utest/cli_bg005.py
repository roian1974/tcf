from src.com.fwk.business.tcf import tcf_sp_bg001
from src.big.sp_bg001.transfer import bg1000cdto
import pandas as pd
from sklearn.model_selection import train_test_split

indto = bg1000cdto
indto.train_file_path = './lang/train/*.txt'
indto.test_file_path = './lang/test/*.txt'
indto.domain_function = "catchLANG"
indto.model_type = 'MLPClassifier'   # svc AdaBoostClassifier Randomforest
argv=['tcf_sp_bg001.py', 'sp_bg001', 'BIG1000', indto ]
tcf_sp_bg001.main(argv)

# 관련 사이트
# http://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html