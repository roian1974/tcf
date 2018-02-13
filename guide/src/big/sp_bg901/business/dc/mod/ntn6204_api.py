import numpy as np
import scipy.io as sio
import tensorflow as tf
import random
from src.com.fwk.business.util.logging import comlogging
from src.big.sp_bg901.business.dc.mod import ntn6204_params
from src.big.sp_bg901.business.dc.mod import ntn6204_input


def inference(batch_placeholders, corrupt_placeholder, init_word_embeds, entity_to_wordvec, num_entities, num_relations, slice_size, batch_size, is_eval, label_placeholders):
    print("Beginning building inference:")
    # TODO: We need to check the shapes and axes used here!

    print("Creating variables")
    d = 100  # embed_size
    k = slice_size
    ten_k = tf.constant([k])
    num_words = len(init_word_embeds)
    E = tf.Variable(init_word_embeds)  # d=embed size
    W = [tf.Variable(tf.truncated_normal([d, d, k])) for r in range(num_relations)]
    V = [tf.Variable(tf.zeros([k, 2 * d])) for r in range(num_relations)]
    b = [tf.Variable(tf.zeros([k, 1])) for r in range(num_relations)]
    U = [tf.Variable(tf.ones([1, k])) for r in range(num_relations)]

    print("Calcing ent2word")
    # python list of tf vectors: i -> list of word indices cooresponding to entity i
    ent2word = [tf.constant(entity_i) - 1 for entity_i in entity_to_wordvec]

    for entword in ent2word:
        continue

    # (num_entities, d) matrix where row i cooresponds to the entity embedding (word embedding average) of entity i
    print("Calcing entEmbed...")
    entEmbed = tf.stack([tf.reduce_mean(tf.gather(E, entword), 0) for entword in ent2word])
    # entEmbed = tf.truncated_normal([num_entities, d])
    print(entEmbed.get_shape())

    predictions = list()
    print("Beginning relations loop")
    for r in range(num_relations):
        print("Relations loop " + str(r))
        e1, e2, e3 = tf.split(1, 3,
                              tf.cast(batch_placeholders[r], tf.int32))  # TODO: should the split dimension be 0 or 1?
        #        e1v = tf.transpose(tf.squeeze(tf.gather(entEmbed, e1, name='e1v'+str(r)),[1]))
        #        e2v = tf.transpose(tf.squeeze(tf.gather(entEmbed, e2, name='e2v'+str(r)),[1]))
        #        e3v = tf.transpose(tf.squeeze(tf.gather(entEmbed, e3, name='e3v'+str(r)),[1]))

        e1v = tf.transpose(tf.squeeze(tf.gather(entEmbed, e1, name='e1v' + str(r))))
        e2v = tf.transpose(tf.squeeze(tf.gather(entEmbed, e2, name='e2v' + str(r))))
        e3v = tf.transpose(tf.squeeze(tf.gather(entEmbed, e3, name='e3v' + str(r))))

        e1v_pos = e1v
        e2v_pos = e2v
        e1v_neg = e1v
        e2v_neg = e3v
        #        num_rel_r = tf.expand_dims(tf.shape(e1v_pos)[1], 0)
        num_rel_r = tf.expand_dims(tf.shape(e1v_pos)[0], 0)
        preactivation_pos = list()
        preactivation_neg = list()

        # print("e1v_pos: "+str(e1v_pos.get_shape()))
        # print("W[r][:,:,slice]: "+str(W[r][:,:,0].get_shape()))
        # print("e2v_pos: "+str(e2v_pos.get_shape()))

        # print("Starting preactivation funcs")
        for slice in range(k):
            preactivation_pos.append(tf.reduce_sum(e1v_pos * tf.matmul(W[r][:, :, slice], e2v_pos), 0))
            preactivation_neg.append(tf.reduce_sum(e1v_neg * tf.matmul(W[r][:, :, slice], e2v_neg), 0))

        preactivation_pos = tf.stack(preactivation_pos)
        preactivation_neg = tf.stack(preactivation_neg)

        temp2_pos = tf.matmul(V[r], tf.concat(0, [e1v_pos, e2v_pos]))
        temp2_neg = tf.matmul(V[r], tf.concat(0, [e1v_neg, e2v_neg]))

        # print("   temp2_pos: "+str(temp2_pos.get_shape()))
        preactivation_pos = preactivation_pos + temp2_pos + b[r]
        preactivation_neg = preactivation_neg + temp2_neg + b[r]

        # print("Starting activation funcs")
        activation_pos = tf.tanh(preactivation_pos)
        activation_neg = tf.tanh(preactivation_neg)

        score_pos = tf.reshape(tf.matmul(U[r], activation_pos), num_rel_r)
        score_neg = tf.reshape(tf.matmul(U[r], activation_neg), num_rel_r)
        # print("score_pos: "+str(score_pos.get_shape()))
        if not is_eval:
            predictions.append(tf.stack([score_pos, score_neg]))
        else:
            predictions.append(tf.stack([score_pos, tf.reshape(label_placeholders[r], num_rel_r)]))
        # print("score_pos_and_neg: "+str(predictions[r].get_shape()))

    # print("Concating predictions")
    predictions = tf.concat(1, predictions)
    # print(predictions.get_shape())

    return predictions

def loss(predictions, regularization):

    print("Beginning building loss")
    temp1 = tf.maximum(tf.sub(predictions[1, :], predictions[0, :]) + 1, 0)
    temp1 = tf.reduce_sum(temp1)

    temp2 = tf.sqrt(sum([tf.reduce_sum(tf.square(var)) for var in tf.trainable_variables()]))

    temp = temp1 + (regularization * temp2)

    return temp

def training(loss, learningRate):
    print("Beginning building training")

    return tf.train.AdagradOptimizer(learningRate).minimize(loss)


def eval(predictions):
    print("predictions "+str(predictions.get_shape()))
    inference, labels = tf.split(0, 2, predictions)
    #inference = tf.transpose(inference)
    #inference = tf.concat((1-inference), inference)
    #labels = ((tf.cast(tf.squeeze(tf.transpose(labels)), tf.int32))+1)/2
    #print("inference "+str(inference.get_shape()))
    #print("labels "+str(labels.get_shape()))
    # get number of correct labels for the logits (if prediction is top 1 closest to actual)
    #correct = tf.nn.in_top_k(inference, labels, 1)
    # cast tensor to int and return number of correct labels
    #return tf.reduce_sum(tf.cast(correct, tf.int32))
    return inference, labels


def get_batch(batch_size, data, num_entities, corrupt_size):
    random_indices = random.sample(range(len(data)), batch_size)
    #data[i][0] = e1, data[i][1] = r, data[i][2] = e2, random=e3 (corrupted)
    batch = [(data[i][0], data[i][1], data[i][2], random.randint(0, num_entities-1))\
	for i in random_indices for j in range(corrupt_size)]
    return batch

def split_batch(data_batch, num_relations):
    batches = [[] for i in range(num_relations)]
    for e1,r,e2,e3 in data_batch:
        batches[r].append((e1,e2,e3))
    return batches

def fill_feed_dict(batches, train_both, batch_placeholders, label_placeholders, corrupt_placeholder):
    feed_dict = {corrupt_placeholder: [train_both and np.random.random()>0.5]}
    for i in range(len(batch_placeholders)):
        feed_dict[batch_placeholders[i]] = batches[i]
        feed_dict[label_placeholders[i]] = [[0.0] for j in range(len(batches[i]))]
    return feed_dict


def load_training_data(data_path = ntn6204_params.data_path) :
    try:
        rtn = True
        training_file = open(data_path + ntn6204_input.training_string)
        training_data = [line.split('\t') for line in training_file.read().strip().split('\n')]

    except Exception as err:
        comlogging.logger.error('▲load_training_data()-ERR:'+ str(err))
        rtn = False
    else:
        comlogging.logger.info('▲load_training_data()-성공:')
    finally:
        if rtn == True :
            return np.array(training_data)
        else :
            return False


#input: path of dataset to be used
#output: python list of entities in dataset
def load_entities( data_path=ntn6204_params.data_path ):
    try:
        rtn = True
        entities_file = open(data_path + ntn6204_input.entities_string)
        entities_list = entities_file.read().strip().split('\n')
        entities_file.close()

    except Exception as err:
        comlogging.logger.error('▲load_entities()-ERR:'+ str(err))
        rtn = False
    else:
        comlogging.logger.info('▲load_entities()-성공:')
    finally:
        if rtn == True :
            return entities_list
        else :
            return False


#input: path of dataset to be used
#output: python list of relations in dataset
def load_relations( data_path=ntn6204_params.data_path ):
    try:
        rtn = True
        relations_file = open(data_path + ntn6204_input.relations_string)
        relations_list = relations_file.read().strip().split('\n')
        relations_file.close()
    except Exception as err:
        comlogging.logger.error('▲load_relations()-ERR:'+ str(err))
        rtn = False
    else:
        comlogging.logger.info('▲load_relations()-성공:')
    finally:
        if rtn == True :
            return relations_list
        else :
            return False

def data_to_indexed(data, entities, relations):
    try:
        rtn = True
        entity_to_index = {entities[i] : i for i in range(len(entities))}
        relation_to_index = {relations[i] : i for i in range(len(relations))}
        indexed_data = [(entity_to_index[data[i][0]], relation_to_index[data[i][1]],entity_to_index[data[i][2]]) for i in range(len(data))]

    except Exception as err:
        comlogging.logger.error('▲preAnalysis()-ERR:'+ str(err))
        rtn = False
    else:
        comlogging.logger.info('▲preAnalysis()-성공:')
    finally:
        if rtn == True :
            return indexed_data
        else :
            return False


#input: Generic function to load embeddings from a .mat file
def load_embeds(file_path):
    try :
        mat_contents = sio.loadmat(file_path)
        words = mat_contents['words']
        we = mat_contents['We']
        tree = mat_contents['tree']
        word_vecs = [[we[j][i] for j in range(ntn6204_params.embedding_size)] for i in range(len(words[0]))]
        entity_words = [map(int, tree[i][0][0][0][0][0]) for i in range(len(tree))]
        rt_list = []
        for xxx in entity_words:
            rt_list.append(list(xxx))
    except Exception as err:
        comlogging.logger.error('▲load_embeds()-ERR:' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲load_embeds()-성공:')
    finally:
        if rtn == True:
            #return (word_vecs,entity_words)
            return (word_vecs,rt_list)

#input: path of dataset to be used
#output: python dict from entity string->1x100 vector embedding of entity as precalculated
def load_init_embeds(data_path=ntn6204_params.data_path):
    try:
        rtn = True
        embeds_path = data_path + ntn6204_input.embeds_string
    except Exception as err:
        comlogging.logger.error('▲load_init_embeds()-ERR:'+ str(err))
        rtn = False
    else:
        comlogging.logger.info('▲load_init_embeds()-성공:')
    finally:
        if rtn == True :
            return load_embeds(embeds_path)
        else :
            return False