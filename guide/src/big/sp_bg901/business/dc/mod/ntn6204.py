import pandas as pd
import pickle
import tensorflow as tf
import datetime
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.common import comutil
from src.big.sp_bg901.business.dc.mod import ntn6204_api

def train(incdto, ntn6204_params) :
    try:
        rtn = True
        _big9006cdto = incdto
        d_big9006dcto = _big9006cdto.getDic()

        num_entities = len(d_big9006dcto['ddto']['entities_list'])  # wordnet : 38696
        num_relations = len(d_big9006dcto['ddto']['relations_list'])  # wordnet : 11
        init_word_embeds = d_big9006dcto['ddto']['init_word_embeds']
        entity_to_wordvec = d_big9006dcto['ddto']['entity_to_wordvec']
        indexed_training_data = d_big9006dcto['ddto']['indexed_training_data']

        num_iters = ntn6204_params.num_iter
        batch_size = ntn6204_params.batch_size
        corrupt_size = ntn6204_params.corrupt_size
        slice_size = ntn6204_params.slice_size

        with tf.Graph().as_default():
            print("Starting to build graph " + str(datetime.datetime.now()))
            batch_placeholders = [tf.placeholder(tf.int32, shape=(None, 3), name='batch_' + str(i)) for i in
                                  range(num_relations)]
            label_placeholders = [tf.placeholder(tf.float32, shape=(None, 1), name='label_' + str(i)) for i in
                                  range(num_relations)]

            corrupt_placeholder = tf.placeholder(tf.bool, shape=(1))  # Which of e1 or e2 to corrupt?

            inference = ntn6204_api.inference(batch_placeholders, corrupt_placeholder, init_word_embeds, entity_to_wordvec,
                                      num_entities, num_relations, slice_size, batch_size, False, label_placeholders)

            loss = ntn6204_api.loss(inference, ntn6204_params.regularization)
            training = ntn6204_api.training(loss, ntn6204_params.learning_rate)

        # Create a session for running Ops on the Graph.
        sess = tf.Session()

        # Run the Op to initialize the variables.
        init = tf.global_variables_initializer()
        sess.run(init)
        saver = tf.train.Saver(tf.trainable_variables())
        for i in range(1, num_iters):
            print("Starting iter " + str(i) + " " + str(datetime.datetime.now()))
            data_batch = ntn6204_api.get_batch(batch_size, indexed_training_data, num_entities, corrupt_size)
            relation_batches = ntn6204_api.split_batch(data_batch, num_relations)

            if i % ntn6204_params.save_per_iter == 0:
                saver.save(sess, ntn6204_params.output_path + "/" + ntn6204_params.data_name + str(i) + '.sess')

            feed_dict = ntn6204_api.fill_feed_dict(relation_batches, ntn6204_params.train_both, batch_placeholders, label_placeholders, corrupt_placeholder)
            _, loss_value = sess.run([training, loss], feed_dict=feed_dict)

            # TODO: Eval against dev set?

        # TODO : 모델을 저장하는 과정을 가진다.
        # comlogging.logger.info("    • Training 3 단계-NTN6204 모델를 파일로 저장")
        # moutfile = "C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\\" + "mod.logistic." + comutil.getsysdate()
        # voutfile = "C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\\" + "vec.logistic." + comutil.getsysdate()
        # basicmodel = list()
        # basicvectorizer = CountVectorizer(ngram_range=(1, 1))
        # 
        # with open(moutfile, 'wb') as f:
        #     pickle.dump(basicmodel, f)
        # 
        # with open(voutfile, 'wb') as f:
        #     pickle.dump(basicvectorizer, f)


    except Exception as err:
        rtn = False
        comlogging.logger.error( 'execute' + str(err))
    else:
        comlogging.logger.info( 'execute-성공-')
    finally:
        
        if rtn == True :
            return True
        else :
            return False

def test(incdto) :
    try:
        rtn = True

        comlogging.logger.info("    • Training 3 단계-테스트데이터를 적용해 본다.")

        moutfile="C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\\" + "mod.navie." + comutil.getsysdate()
        voutfile = "C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\\" + "vec.navie." + comutil.getsysdate()

        with open(moutfile, 'rb') as f:
            testmodel = pickle.load( f )

        with open(voutfile, 'rb') as f:
            testvector = pickle.load( f )

        testvectorizer = testvector
        basictest = testvectorizer.transform(incdto)
        predictions = testmodel.predict(basictest.toarray())

        out = pd.crosstab(train["Label"], predictions, rownames=["Actual"], colnames=["Predicted"])
        comlogging.logger.info( "\n===========================\n" + str(out) )
        out = pd.crosstab(train["Label"], predictions, rownames=["Actual"], colnames=["Predicted"])

        total = out[0][0] + out[0][1] + out[1][0] + out[1][1]
        accuracy =  ( out[0][0]+ out[1][1] ) / total
        comlogging.logger.info("accuracy:" + str(accuracy))

    except Exception as err:
        rtn = False
        comlogging.logger.error( 'execute' + str(err))
    else:
        comlogging.logger.info( 'execute-성공-')
    finally:
        if rtn == True :
            return out
        else :
            return False


