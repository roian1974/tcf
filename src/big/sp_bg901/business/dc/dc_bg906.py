from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.info import include
from src.big.sp_bg901.business.dc.mod import ntn6204_api
from src.big.sp_bg901.business.dc.mod import ntn6204

def preAnalysis(indto) :
    try:
        rtn = True
        _big9006cdto = indto
        d_big9006cdto = _big9006cdto.getDic()

        data_path = d_big9006cdto['params']['data_path']

        raw_training_data = ntn6204_api.load_training_data(data_path)  # wordnet : 112581 * 3

        print("Load entities and relations...")
        entities_list = ntn6204_api.load_entities(data_path)  # wordnet : 38696
        relations_list = ntn6204_api.load_relations(data_path)  # wordnet : 11

        # python list of (e1, R, e2) for entire training set in index form
        indexed_training_data = ntn6204_api.data_to_indexed(raw_training_data, entities_list, relations_list)

        print("Load embeddings...")
        (init_word_embeds, entity_to_wordvec) = ntn6204_api.load_init_embeds(data_path)

        # ddto 셋팅
        _big9006cdto.set_raw_training_data(raw_training_data)
        _big9006cdto.set_entities_list(entities_list)
        _big9006cdto.set_relations_list(relations_list)
        _big9006cdto.set_indexed_training_data(indexed_training_data)
        _big9006cdto.set_init_word_embeds(init_word_embeds)
        _big9006cdto.set_entity_to_wordvec(entity_to_wordvec)

    except Exception as err:
        comlogging.logger.error('▲preAnalysis()-ERR:'+ str(err))
        include.setErr('EBIG005', 'preAnalysis 분석에러' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲preAnalysis()-성공:')
    finally:
        if rtn == True :
            return _big9006cdto
        else :
            return False

def trainModel(indto, ntn6204_params) :
    try:
        _big9006cdto = indto
        modelType = _big9006cdto.getDic()['modelType']
        rtn = True
        if modelType == "NTN6204" :
            ntn6204.train(_big9006cdto, ntn6204_params)
        elif modelType == "NaiveEyes" :
            ntn6204.train(_big9006cdto, ntn6204_params)
        elif modelType == "RF":
            ntn6204.train(_big9006cdto, ntn6204_params)
        elif modelType == "SVMGusian":
            ntn6204.train(_big9006cdto, ntn6204_params)
        elif modelType == "SVMLinear":
            ntn6204.train(_big9006cdto, ntn6204_params)
        else :
            pass

    except Exception as err:
        comlogging.logger.error('▲exeModel()-ERR:'+ str(err))
        include.setErr('EBIG005', 'exeModel 수행 에러' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲exeModel()-성공:')
    finally:
        if rtn == True :
            return True
        else :
            return False
