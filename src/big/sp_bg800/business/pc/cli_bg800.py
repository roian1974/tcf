from pprint import pprint
from src.big.sp_bg800.transfer.big8001cdto import BIG8001CDTO
from src.com.fwk.business.tcf import tcf_sp_bg001

#
# _big8001cdto = BIG8001CDTO()
# _big8001cdto.trainfile = 'titanic_train.csv'
# _big8001cdto.model_type = 'Name'
# argv=['tcf_sp_bg001.py', 'sp_bg800', 'BIG8001', _big8001cdto ]
# tcf_sp_bg001.main(argv)

# _big8001cdto = BIG8001CDTO()
# _big8001cdto.trainfile = 'titanic_train.csv'
# _big8001cdto.model_type = 'Sex'
# argv=['tcf_sp_bg001.py', 'sp_bg800', 'BIG8001', _big8001cdto ]
# tcf_sp_bg001.main(argv)

# _big8001cdto = BIG8001CDTO()
# _big8001cdto.trainfile = 'titanic_train.csv'
# _big8001cdto.model_type = 'Age'
# argv=['tcf_sp_bg001.py', 'sp_bg800', 'BIG8001', _big8001cdto ]
# tcf_sp_bg001.main(argv)

# _big8001cdto = BIG8001CDTO()
# _big8001cdto.trainfile = 'titanic_train.csv'
# _big8001cdto.model_type = 'Binning'
# argv=['tcf_sp_bg001.py', 'sp_bg800', 'BIG8001', _big8001cdto ]
# tcf_sp_bg001.main(argv)

# _big8001cdto = BIG8001CDTO()
# _big8001cdto.trainfile = 'titanic_train.csv'
# _big8001cdto.model_type = 'Fare'
# argv=['tcf_sp_bg001.py', 'sp_bg800', 'BIG8001', _big8001cdto ]
# tcf_sp_bg001.main(argv)

# _big8001cdto = BIG8001CDTO()
# _big8001cdto.trainfile = 'titanic_train.csv'
# _big8001cdto.model_type = 'Cabin'
# argv=['tcf_sp_bg001.py', 'sp_bg800', 'BIG8001', _big8001cdto ]
# tcf_sp_bg001.main(argv)


# _big8001cdto = BIG8001CDTO()
# _big8001cdto.trainfile = 'titanic_train.csv'
# _big8001cdto.model_type = 'Familysize'
# argv=['tcf_sp_bg001.py', 'sp_bg800', 'BIG8001', _big8001cdto ]
# tcf_sp_bg001.main(argv)

_big8001cdto = BIG8001CDTO()
_big8001cdto.trainfile = 'titanic_train.csv'
_big8001cdto.model_type = 'KNN'
argv=['tcf_sp_bg001.py', 'sp_bg800', 'BIG8002', _big8001cdto ]
tcf_sp_bg001.main(argv)


# _big8001cdto = BIG8001CDTO()
# _big8001cdto.trainfile = 'titanic_train.csv'
# _big8001cdto.model_type = 'DT'
# argv=['tcf_sp_bg001.py', 'sp_bg800', 'BIG8002', _big8001cdto ]
# tcf_sp_bg001.main(argv)


# _big8001cdto = BIG8001CDTO()
# _big8001cdto.trainfile = 'titanic_train.csv'
# _big8001cdto.testfile = 'titanic_test.csv'
# _big8001cdto.model_type = 'SVM'
# argv=['tcf_sp_bg001.py', 'sp_bg800', 'BIG8003', _big8001cdto ]
# tcf_sp_bg001.main(argv)