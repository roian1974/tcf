import tensorflow as tf
# from src.com.fwk.business.util.shinhan import ntn_input
# from src.com.fwk.business.util.shinhan import ntn
# from src.com.fwk.business.util.shinhan import params
# import random

# Inference
# Loss
# Training


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







