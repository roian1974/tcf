import json
from pprint import pprint
from src.com.fwk.business.util.common import comutil

class BIG9006CDTO :

    data_number = 0
    data_name = 'Wordnet'
    data_path = ''

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
    model_type = 'NTN'

    entities_string = '/entities.txt'
    relations_string = '/relations.txt'
    embeds_string = '/initEmbed01.mat'
    training_string = '/train.txt'
    test_string = '/test.txt'
    dev_string = '/dev.txt'

    raw_training_data = list()
    entities_list = list()
    relations_list = list()
    indexed_training_data = list()
    init_word_embeds = ''
    entity_to_wordvec = list()

    def __init__(self):
        pass


    # --- ddto
    def set_raw_training_data(self,raw_training_data):
        self.raw_training_data = raw_training_data

    def set_entities_list(self,entities_list):
        self.entities_list = entities_list

    def set_relations_list(self,relations_list):
        self.relations_list = relations_list

    def set_init_word_embeds(self,init_word_embeds):
        self.init_word_embeds = init_word_embeds

    def set_entity_to_wordvec(self,entity_to_wordvec):
        self.entity_to_wordvec = entity_to_wordvec
        
    def set_indexed_training_data(self,indexed_training_data):
        self.indexed_training_data

    #--- cdto

    def set_entities_string(self, entities_string):
        self.entities_string

    def set_relations_string(self, relations_string):
        self.relations_string

    def set_embeds_string(self, embeds_string):
        self.embeds_string

    def set_training_string(self, training_string):
        self.training_string

    def set_test_string(self, test_string):
        self.test_string

    def set_dev_string(self, dev_string):
        self.dev_string

    # data_number = 0 - Wordnet, 1 - Freebase
    def set_data_number	(self ,data_number):
        self.data_number = data_number
        if self.data_number == 0:
            self.data_name = 'Wordnet'
        else:
            self.data_name = 'Freebase'

    def set_num_iter(self ,num_iter):
        self.num_iter = num_iter

    def set_data_path(self ,data_path):
        self.data_path = data_path

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

    def set_model_type(self, model_type):
        self.model_type = model_type

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

    def get_model_type(self):
        return self.model_type

    def getDic(self):
        dic = { 'input':{}, 'ddto':{}, 'params':{} }

        dic['params']['data_number'] =self.data_number
        dic['params']['num_iter'] =self.num_iter
        dic['params']['train_both'] =self.train_both
        dic['params']['batch_size'] =self.batch_size
        dic['params']['corrupt_size'] =self.corrupt_size
        dic['params']['embedding_size'] =self.embedding_size
        dic['params']['slice_size'] =self.slice_size
        dic['params']['regularization'] =self.regularization
        dic['params']['in_tensor_keep_normal'] =self.in_tensor_keep_normal
        dic['params']['save_per_iter'] =self.save_per_iter
        dic['params']['learning_rate'] =self.learning_rate
        dic['params']['output_dir'] = self.output_dir
        dic['params']['data_path'] = self.data_path
        dic['params']['model_type'] = self.model_type

        dic['ddto']['raw_training_data'] = self.raw_training_data
        dic['ddto']['entities_list'] = self.entities_list
        dic['ddto']['relations_list'] = self.relations_list
        dic['ddto']['init_word_embeds'] = self.init_word_embeds
        dic['ddto']['entity_to_wordvec'] = self.entity_to_wordvec

        dic['input']['entities_string'] = self.entities_string
        dic['input']['relations_string'] = self.relations_string
        dic['input']['embeds_string'] = self.embeds_string
        dic['input']['training_string'] = self.training_string
        dic['input']['test_string'] = self.test_string
        dic['input']['dev_string'] = self.dev_string

        return dic

    def setJson(self,file):
        file = "C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\\" + "big9006cdto.json"
        dic = self.loadJson(file)

        self.data_number = dic['params']['data_number']
        if self.data_number == 0:
            self.data_name = 'Wordnet'
        else:
            self.data_name = 'Freebase'

        self.num_iter = dic['params']['num_iter']
        self.train_both = dic['params']['train_both']
        self.batch_size = dic['params']['batch_size']
        self.corrupt_size = dic['params']['corrupt_size']
        self.embedding_size = dic['params']['embedding_size']
        self.slice_size = dic['params']['slice_size']
        self.regularization = dic['params']['regularization']
        self.in_tensor_keep_normal = dic['params']['in_tensor_keep_normal']
        self.save_per_iter = dic['params']['save_per_iter']
        self.learning_rate = dic['params']['learning_rate']
        self.output_dir = dic['params']['output_dir']
        self.data_path = dic['params']['data_path']
        self.model_type = dic['params']['model_type']

        self.raw_training_data = dic['ddto']['raw_training_data']
        self.entities_list = dic['ddto']['entities_list']
        self.relations_list = dic['ddto']['relations_list']
        self.init_word_embeds = dic['ddto']['init_word_embeds']
        self.entity_to_wordvec = dic['ddto']['entity_to_wordvec']

        self.entities_string = dic['input']['entities_string']
        self.relations_string = dic['input']['relations_string']
        self.embeds_string = dic['input']['embeds_string']
        self.training_string = dic['input']['training_string']
        self.test_string = dic['input']['test_string']
        self.dev_string = dic['input']['dev_string']

    def getBIG9006CDTO(self,dic):
        self.data_number = dic['params']['data_number']
        self.num_iter = dic['params']['num_iter']
        self.train_both = dic['params']['train_both']
        self.batch_size = dic['params']['batch_size']
        self.corrupt_size = dic['params']['corrupt_size']
        self.embedding_size = dic['params']['embedding_size']
        self.slice_size = dic['params']['slice_size']
        self.regularization = dic['params']['regularization']
        self.in_tensor_keep_normal = dic['params']['in_tensor_keep_normal']
        self.save_per_iter = dic['params']['save_per_iter']
        self.learning_rate = dic['params']['learning_rate']
        self.output_dir = dic['params']['output_dir']
        self.data_path = dic['params']['data_path']
        self.model_type = dic['params']['model_type']

        self.raw_training_data = dic['ddto']['raw_training_data']
        self.entities_list = dic['ddto']['entities_list']
        self.relations_list = dic['ddto']['relations_list']
        self.init_word_embeds = dic['ddto']['init_word_embeds']
        self.entity_to_wordvec = dic['ddto']['entity_to_wordvec']

        self.entities_string = dic['input']['entities_string']
        self.relations_string = dic['input']['relations_string']
        self.embeds_string = dic['input']['embeds_string']
        self.training_string = dic['input']['training_string']
        self.test_string = dic['input']['test_string']
        self.dev_string = dic['input']['dev_string']

    def dumpJson(self):
            dic = self.getDic()
            with open('C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\\'+"big9006cdto.json", 'w') as fp:
                json.dump(dic, fp)


    def loadJson(self,file):
        # file = "C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\\"+"big9006cdto.json"
        with open(file) as data_file:
            data = json.load(data_file)
        # pprint(data)

        return data




