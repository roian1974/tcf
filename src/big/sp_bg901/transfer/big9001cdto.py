from src.com.fwk.business.util.common import comutil

class BIG9001CDTO :
    data_number = 0
    data_name = 'Wordnet'
    num_iter = 500
    train_both = False
    batch_size = 20000
    corrupt_size = 10  # how many negative examples are given for each positive example?
    embedding_size = 100
    slice_size = 3  # depth of tensor for each relation
    regularization = 0.0001  # parameter \lambda used in L2 normalization
    in_tensor_keep_normal = False
    save_per_iter = 10
    learning_rate = 0.01
    output_dir = ''

    def __init__(self):
        pass

    # data_number = 0 - Wordnet, 1 - Freebase
    def set_data_number	(self ,data_number):
        self.data_number = data_number
        if self.data_number == 0:
            self.data_name = 'Wordnet'
        else:
            self.data_name = 'Freebase'

    def set_num_iter(self ,num_iter):
        self.num_iter = num_iter

    def set_train_both(self ,train_both):
        self.train_both = train_both

    def set_batch_size(self ,batch_size):
        self.batch_size = batch_size

    def set_corrupt_size(self ,corrupt_size):
        self.corrupt_size  = corrupt_size

    def set_embedding_size(self ,embedding_size):
        self.embedding_size = embedding_size

    def set_slice_size(self ,slice_size):
        self.slice_size = slice_size

    def set_regularization(self ,regularization):
        self.regularization = regularization

    def set_in_tensor_keep_normal	(self ,in_tensor_keep_normal	):
        self.in_tensor_keep_normal = in_tensor_keep_normal

    def set_save_per_iter(self ,save_per_iter):
        self.save_per_iter = save_per_iter

    def set_learning_rate(self ,learning_rate):
        self.learning_rate = learning_rate

    def set_output_dir(self,output_dir):
        self.output_dir = output_dir

    def get_data_number(self):
        return self.data_number
    def get_num_iter(self):
        return self.num_iter

    def get_train_both(self):
        return self.train_both

    def get_batch_size(self):
        return self.batch_size

    def get_corrupt_size(self):
        return self.corrupt_size

    def get_embedding_size(self):
        return self.embedding_size

    def get_slice_size(self):
        return self.slice_size

    def get_regularization(self):
        return self.regularization

    def get_in_tensor_keep_normal(self):
        return self.in_tensor_keep_normal

    def get_save_per_iter(self):
        return self.save_per_iter

    def get_learning_rate(self):
        return self.learning_rate

    def get_output_dir(self):
        return self.output_dir

    def getDic(self):
        dic = {}
        dic['data_number'] =self.data_number
        dic['num_iter'] =self.num_iter
        dic['train_both'] =self.train_both
        dic['batch_size'] =self.batch_size
        dic['corrupt_size'] =self.corrupt_size
        dic['embedding_siz'] =self.embedding_siz
        dic['slice_size'] =self.slice_size
        dic['regularizatio'] =self.regularizatio
        dic['in_tensor_keep_norma'] =self.in_tensor_keep_norma
        dic['save_per_iter'] =self.save_per_iter
        dic['learning_rate'] =self.learning_rate
        dic['output_dir'] = self.output_dir

        return dic





