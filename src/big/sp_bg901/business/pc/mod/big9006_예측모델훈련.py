import time
from pprint import pprint

from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.big.sp_bg901.transfer.big9006cdto import BIG9006CDTO
from src.big.sp_bg901.business.dc import dc_bg906
from src.big.sp_bg901.business.dc.mod import ntn6204_params, ntn6204_input


def BIG9006():
    rtn = True
    try:
        comlogging.logger.info( "BIG9006_start() start ")
        indto, ntn6204_params = BIG9006_start()
        if indto != False :
            comlogging.logger.info( "BIG9006_processing() start ")
            BIG9006_processing(indto, ntn6204_params)
        else :
            raise Exception('BIG9006_start 함수에서 에러가 발생')
    except Exception as err:
        comlogging.logger.error( 'BIG9006-'+ str(err))
        include.setErr('EBIG9006', 'BIG9006' + str(err))
    else:
        comlogging.logger.info( 'BIG9006-성공')
    finally:
        BIG9006_end()

        if include.isError() == False :
            return True
        else :
            return False

def BIG9006_start() :
    try:

        indto = BIG9006CDTO()
        dic = include.gcominfo['sysargv'][3]

        pprint(dic)

        indto.getBIG9006CDTO(dic)

        d_big9006cdto = indto.getDic()
        ntn6204_params.data_path = d_big9006cdto['params']['data_path']
        ntn6204_params.output_dir = d_big9006cdto['params']['output_dir']
        ntn6204_params.num_iter = d_big9006cdto['params']['num_iter']
        ntn6204_params.train_both = d_big9006cdto['params']['train_both']
        ntn6204_params.batch_size = d_big9006cdto['params']['batch_size']
        ntn6204_params.corrupt_size = d_big9006cdto['params']['corrupt_size']
        ntn6204_params.embedding_size = d_big9006cdto['params']['embedding_size']
        ntn6204_params.slice_size = d_big9006cdto['params']['slice_size']
        ntn6204_params.regularization = d_big9006cdto['params']['regularization']
        ntn6204_params.in_tensor_keep_normal = d_big9006cdto['params']['in_tensor_keep_normal']
        ntn6204_params.save_per_iter = d_big9006cdto['params']['save_per_iter']
        ntn6204_params.learning_rate = d_big9006cdto['params']['learning_rate']

        ntn6204_input.entities_string = d_big9006cdto['input']['entities_string']
        ntn6204_input.relations_string = d_big9006cdto['input']['relations_string']
        ntn6204_input.embeds_string = d_big9006cdto['input']['embeds_string']
        ntn6204_input.training_string = d_big9006cdto['input']['training_string']
        ntn6204_input.test_string = d_big9006cdto['input']['test_string']
        ntn6204_input.dev_string = d_big9006cdto['input']['dev_string']

    except Exception as err:
        comlogging.logger.error( 'BIG9006_start-' + str(err))
        include.setErr('EBIG9006', 'BIG9006_start,' + str(err))
    else:
        comlogging.logger.info( 'BIG9006_start-성공')
    finally:
        if include.isError() == False :
            return indto, ntn6204_params
        else :
            return False


def BIG9006_start_ty2():
    try:

        indto = BIG9006CDTO()

        indto.set_data_number(0)

        data_name = include.gcominfo['sysargv'][3]
        data_path = "C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\\" + data_name
        indto.set_data_path(include.gcominfo[data_path])  # data_path = './data/'+data_name

        output_path = "C:\jDev\MyWorks\PycharmProjects\Roian\log\output\\big\\" + data_name  # output_path = './output/' + data_name + '/'
        indto.set_output_dir(output_path)

        # 모델 파리미터 정보 셋팅
        indto.set_num_iter(int(500))
        indto.set_train_both(False)
        indto.set_batch_size(200000)
        indto.set_corrupt_size(10)
        indto.set_embedding_size(100)
        indto.set_slice_size(3)
        indto.set_regularization(0.0001)
        indto.set_in_tensor_keep_normal(False)
        indto.set_save_per_iter(10)
        indto.set_learning_rate(0.01)
        indto.set_model_type('NTN6204')

        # 모델 입력값 셋팅
        indto.set_entities_string('/entities.txt')
        indto.set_relations_string('/relations.txt')
        indto.set_embeds_string('/initEmbed01.mat')
        indto.set_training_string('/train.txt')
        indto.set_test_string('/test.txt')
        indto.set_dev_string('/dev.txt')

        d_big9006cdto = indto.getDic()
        ntn6204_params.data_path = d_big9006cdto['params']['data_path']
        ntn6204_params.output_dir = d_big9006cdto['params']['output_dir']
        ntn6204_params.num_iter = d_big9006cdto['params']['num_iter']
        ntn6204_params.train_both = d_big9006cdto['params']['train_both']
        ntn6204_params.batch_size = d_big9006cdto['params']['batch_size']
        ntn6204_params.corrupt_size = d_big9006cdto['params']['corrupt_size']
        ntn6204_params.embedding_size = d_big9006cdto['params']['embedding_size']
        ntn6204_params.slice_size = d_big9006cdto['params']['slice_size']
        ntn6204_params.regularization = d_big9006cdto['params']['regularization']
        ntn6204_params.in_tensor_keep_normal = d_big9006cdto['params']['in_tensor_keep_normal']
        ntn6204_params.save_per_iter = d_big9006cdto['params']['save_per_iter']
        ntn6204_params.learning_rate = d_big9006cdto['params']['learning_rate']

        ntn6204_input.entities_string = d_big9006cdto['input']['entities_string']
        ntn6204_input.relations_string = d_big9006cdto['input']['relations_string']
        ntn6204_input.embeds_string = d_big9006cdto['input']['embeds_string']
        ntn6204_input.training_string = d_big9006cdto['input']['training_string']
        ntn6204_input.test_string = d_big9006cdto['input']['test_string']
        ntn6204_input.dev_string = d_big9006cdto['input']['dev_string']

    except Exception as err:
        comlogging.logger.error('BIG9006_start-' + str(err))
        include.setErr('EBIG9006', 'BIG9006_start,' + str(err))
    else:
        comlogging.logger.info('BIG9006_start-성공')
    finally:
        if include.isError() == False:
            return indto, ntn6204_params
        else:
            return False


def BIG9006_processing(indto, params) :
    try:
        comlogging.logger.info("#################################################################" + str(getIntTime()))

        _big9006cdto = indto
        ntn6204_params = params
        _big9006cdto = dc_bg906.preAnalysis(_big9006cdto)

        if _big9006cdto  != True :
            dc_bg906.trainModel(_big9006cdto, ntn6204_params)

        comlogging.logger.info("#################################################################" + str(getIntTime()))
    except Exception as err:
        comlogging.logger.error( 'BIG9006_processing '+ str(err) )
        include.setErr('EBIG9006', 'BIG9006_processing,' + str(err))
    else:
        comlogging.logger.info( 'BIG9006_processing-성공')
    finally:
        if include.isError() == False :
            return True
        else :
            return False

def BIG9006_end() :
    try:
        pass
    except Exception as err:
        comlogging.logger.error( 'BIG9006_end '+ str(err))
        include.setErr('EBIG9006', 'BIG9006_end,' + str(err))
    else:
        comlogging.logger.info( 'BIG9006_end-성공')
    finally:

        if include.isError() == False :
            return True
        else :
            return False

#-----------------------------------------------------------------------------------------------------------------------

def getTime():
    t3 = time.localtime()
    return '{}년{}월{}일-{}시{}분{}초'.format(t3.tm_year, t3.tm_mon, t3.tm_mday,t3.tm_hour, t3.tm_min, t3.tm_sec)

def getIntTime():
    return time.mktime(time.localtime())
