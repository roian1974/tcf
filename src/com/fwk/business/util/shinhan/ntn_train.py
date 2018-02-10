# import tensorflow as tf
from src.com.fwk.business.util.shinhan import ntn_input, ntn, params
# import numpy as np
# import numpy.matlib
import random
import datetime

# functions.py

import tensorflow as tf
import functools, operator

def getLength(t):
    temp = (dim.value for dim in t.get_shape())         # dim is Dimension class.
    return functools.reduce(operator.mul, temp)

def showConstant(t):
    sess = tf.InteractiveSession()
    print(t.eval())
    sess.close()

def showConstantDetail(t):
    sess = tf.InteractiveSession()
    print(t.eval())
    print('shape :', tf.shape(t))
    print('size  :', tf.size(t))
    print('rank  :', tf.rank(t))
    print(t.get_shape())

    sess.close()

def showVariable(v):
    sess = tf.InteractiveSession()
    v.initializer.run()
    print(v.eval())
    sess.close()

def var2Numpy(v):
    sess = tf.InteractiveSession()
    v.initializer.run()
    n = v.eval()
    sess.close()

    return n

def op2Numpy(op):
    sess = tf.InteractiveSession()
    init = tf.initialize_all_variables()
    sess.run(init)
    ret = sess.run(op)
    sess.close()

    return ret

def showOperation(op):
    print(op2Numpy(op))



def data_to_indexed(data, entities, relations):
    entity_to_index = {entities[i] : i for i in range(len(entities))}
    relation_to_index = {relations[i] : i for i in range(len(relations))}
    indexed_data = [(entity_to_index[data[i][0]], relation_to_index[data[i][1]],\
            entity_to_index[data[i][2]]) for i in range(len(data))]
    return indexed_data

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


#scw

#returns a (batch_size*corrupt_size, 2) vector corresponding to [g(T^i), g(T_c^i)] for all i
def inference(batch_placeholders, corrupt_placeholder, init_word_embeds, entity_to_wordvec, num_entities, num_relations, slice_size, batch_size, is_eval, label_placeholders):
    print("Beginning building inference:")
    #TODO: We need to check the shapes and axes used here!

    print("Creating variables")
    d = 100 # embed_size
    k = slice_size
    ten_k = tf.constant([k])
    num_words = len(init_word_embeds)
    E = tf.Variable(init_word_embeds) #d=embed size
    W = [tf.Variable(tf.truncated_normal([d,d,k])) for r in range(num_relations)]
    V = [tf.Variable(tf.zeros([k, 2*d])) for r in range(num_relations)]
    b = [tf.Variable(tf.zeros([k, 1])) for r in range(num_relations)]
    U = [tf.Variable(tf.ones([1, k])) for r in range(num_relations)]

    print("Calcing ent2word")
    #python list of tf vectors: i -> list of word indices cooresponding to entity i
    ent2word = [tf.constant(entity_i)-1 for entity_i in entity_to_wordvec]


    for entword in ent2word:
        continue





    #(num_entities, d) matrix where row i cooresponds to the entity embedding (word embedding average) of entity i
    print("Calcing entEmbed...")
    entEmbed = tf.stack([tf.reduce_mean(tf.gather(E, entword), 0) for entword in ent2word])
    #entEmbed = tf.truncated_normal([num_entities, d])
    print(entEmbed.get_shape())

    predictions = list()
    print("Beginning relations loop")
    for r in range(num_relations):
        print("Relations loop "+str(r))
        e1, e2, e3 = tf.split(1, 3, tf.cast(batch_placeholders[r], tf.int32)) #TODO: should the split dimension be 0 or 1?
#        e1v = tf.transpose(tf.squeeze(tf.gather(entEmbed, e1, name='e1v'+str(r)),[1]))
#        e2v = tf.transpose(tf.squeeze(tf.gather(entEmbed, e2, name='e2v'+str(r)),[1]))
#        e3v = tf.transpose(tf.squeeze(tf.gather(entEmbed, e3, name='e3v'+str(r)),[1]))
        
        
        e1v = tf.transpose(tf.squeeze(tf.gather(entEmbed, e1, name='e1v'+str(r))))
        e2v = tf.transpose(tf.squeeze(tf.gather(entEmbed, e2, name='e2v'+str(r))))
        e3v = tf.transpose(tf.squeeze(tf.gather(entEmbed, e3, name='e3v'+str(r))))
        
        
        e1v_pos = e1v
        e2v_pos = e2v
        e1v_neg = e1v
        e2v_neg = e3v
#        num_rel_r = tf.expand_dims(tf.shape(e1v_pos)[1], 0)
        num_rel_r = tf.expand_dims(tf.shape(e1v_pos)[0], 0)
        preactivation_pos = list()
        preactivation_neg = list()

        #print("e1v_pos: "+str(e1v_pos.get_shape()))
        #print("W[r][:,:,slice]: "+str(W[r][:,:,0].get_shape()))
        #print("e2v_pos: "+str(e2v_pos.get_shape()))

        #print("Starting preactivation funcs")
        for slice in range(k):
            preactivation_pos.append(tf.reduce_sum(e1v_pos*tf.matmul(W[r][:,:,slice], e2v_pos), 0))
            preactivation_neg.append(tf.reduce_sum(e1v_neg*tf.matmul( W[r][:,:,slice], e2v_neg), 0))

        preactivation_pos = tf.stack(preactivation_pos)
        preactivation_neg = tf.stack(preactivation_neg)

        temp2_pos = tf.matmul(V[r], tf.concat(0, [e1v_pos, e2v_pos]))
        temp2_neg = tf.matmul(V[r], tf.concat(0, [e1v_neg, e2v_neg]))

        #print("   temp2_pos: "+str(temp2_pos.get_shape()))
        preactivation_pos = preactivation_pos+temp2_pos+b[r]
        preactivation_neg = preactivation_neg+temp2_neg+b[r]

        #print("Starting activation funcs")
        activation_pos = tf.tanh(preactivation_pos)
        activation_neg = tf.tanh(preactivation_neg)

        score_pos = tf.reshape(tf.matmul(U[r], activation_pos), num_rel_r)
        score_neg = tf.reshape(tf.matmul(U[r], activation_neg), num_rel_r)
        #print("score_pos: "+str(score_pos.get_shape()))
        if not is_eval:
            predictions.append(tf.stack([score_pos, score_neg]))
        else:
            predictions.append(tf.stack([score_pos, tf.reshape(label_placeholders[r], num_rel_r)]))
        #print("score_pos_and_neg: "+str(predictions[r].get_shape()))


    #print("Concating predictions")
    predictions = tf.concat(1, predictions)
    #print(predictions.get_shape())

    return predictions


def run_training():
    print("Begin!")
    #python list of (e1, R, e2) for entire training set in string form
    
    print("Load training data...")
    raw_training_data = ntn_input.load_training_data(params.data_path)      # wordnet : 112581 * 3

    print("Load entities and relations...")
    entities_list = ntn_input.load_entities(params.data_path)               # wordnet : 38696
    relations_list = ntn_input.load_relations(params.data_path)             # wordnet : 11
    #python list of (e1, R, e2) for entire training set in index form
    indexed_training_data = data_to_indexed(raw_training_data, entities_list, relations_list)
    # wordnet : 112581 (ex ['__spiritual_bouquet_1' '_type_of' '__sympathy_card_1'] --> (30298, 1, 18628) )

    print("Load embeddings...")
    (init_word_embeds, entity_to_wordvec) = ntn_input.load_init_embeds(params.data_path)

    num_entities = len(entities_list)       # wordnet : 38696
    num_relations = len(relations_list)     # wordnet : 11

    num_iters = params.num_iter
    batch_size = params.batch_size
    corrupt_size = params.corrupt_size
    slice_size = params.slice_size

    with tf.Graph().as_default():
        print("Starting to build graph "+str(datetime.datetime.now()))
        batch_placeholders = [tf.placeholder(tf.int32, shape=(None, 3), name='batch_'+str(i)) for i in range(num_relations)]
        label_placeholders = [tf.placeholder(tf.float32, shape=(None, 1), name='label_'+str(i)) for i in range(num_relations)]

        corrupt_placeholder = tf.placeholder(tf.bool, shape=(1)) #Which of e1 or e2 to corrupt?
        ntn.inference()
        inference = ntn.inference(batch_placeholders, corrupt_placeholder, init_word_embeds, entity_to_wordvec, \
                                  num_entities, num_relations, slice_size, batch_size, False, label_placeholders)
        loss = ntn.loss(inference, params.regularization)
        training = ntn.training(loss, params.learning_rate)

    # Create a session for running Ops on the Graph.
    sess = tf.Session()

    # Run the Op to initialize the variables.
    init = tf.global_variables_initializer()
    sess.run(init)
    saver = tf.train.Saver(tf.trainable_variables())
    for i in range(1, num_iters):
        print("Starting iter "+str(i)+" "+str(datetime.datetime.now()))
        data_batch = get_batch(batch_size, indexed_training_data, num_entities, corrupt_size)
        relation_batches = split_batch(data_batch, num_relations)

        if i % params.save_per_iter == 0:
            saver.save(sess, params.output_path + "/" + params.data_name + str(i) + '.sess')

        feed_dict = fill_feed_dict(relation_batches, params.train_both, batch_placeholders, label_placeholders, corrupt_placeholder)
        _, loss_value = sess.run([training, loss], feed_dict=feed_dict)

        #TODO: Eval against dev set?

def main(argv):
    run_training()

if __name__=="__main__":
    tf.app.run()
