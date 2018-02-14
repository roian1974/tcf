from src.com.fwk.business.tcf import tcf_sp_bg001
from src.big.sp_bg001.transfer.big1000cdto import BIG1000CDTO

servicename='sp_bg001'
hostprog='BIG1003'
userid='user01'
tpfq=200
cdto = BIG1000CDTO(servicename,hostprog,userid,tpfq)

cdto.indata['train_file_path'] = './lang/train/*.txt'
cdto.indata['test_file_path'] = './lang/test/*.txt'
cdto.indata['domain_function'] = "catchLANG"
cdto.indata['model_type'] = 'MLPClassifier'   # svc AdaBoostClassifier Randomforest
argv=['tcf_sp_bg001.py', servicename, hostprog, cdto ]
s_out = tcf_sp_bg001.main(argv)

cdto = s_out['outdata'][0]
print('정확도:',cdto.outdata['accuracy'])
print('보고서:',cdto.outdata['report'])

# 관련 사이트
# http://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html