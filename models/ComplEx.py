# coding:utf-8
import numpy as np
import tensorflow as tf
from .Model import Model


class ComplEx(Model):
    def embedding_def(self):
        config = self.get_config()
        self.ent1_embeddings = tf.get_variable(name="ent1_embeddings", shape=[config.entTotal, config.hidden_size],
                                               initializer=tf.contrib.layers.xavier_initializer(uniform=True))
        self.rel1_embeddings = tf.get_variable(name="rel1_embeddings", shape=[config.relTotal, config.hidden_size],
                                               initializer=tf.contrib.layers.xavier_initializer(uniform=True))
        self.ent2_embeddings = tf.get_variable(name="ent2_embeddings", shape=[config.entTotal, config.hidden_size],
                                               initializer=tf.contrib.layers.xavier_initializer(uniform=True))
        self.rel2_embeddings = tf.get_variable(name="rel2_embeddings", shape=[config.relTotal, config.hidden_size],
                                               initializer=tf.contrib.layers.xavier_initializer(uniform=True))
        self.parameter_lists = {"ent_re_embeddings": self.ent1_embeddings,
                                "ent_im_embeddings": self.ent2_embeddings,
                                "rel_re_embeddings": self.rel1_embeddings,
                                "rel_im_embeddings": self.rel2_embeddings}

    r'''
    ComplEx extends DistMult by introducing complex-valued embeddings so as to better model asymmetric relations.
    It is proved that HolE is subsumed by ComplEx as a special case.
    '''

    def _calc(self, h, t, r):
        return tf.real(h * t * tf.conj(r))

    def loss_def(self):
        # Obtaining the initial configuration of the model
        config = self.get_config()
        # To get positive triples and negative triples for training
        # To get labels for the triples, positive triples as 1 and negative triples as -1
        # The shapes of h, t, r, y are (batch_size, 1 + negative_ent + negative_rel)
        h, t, r = self.get_all_instance()
        y = self.get_all_labels()
        # Embedding entities and relations of triples
        e1_h = tf.nn.embedding_lookup(self.ent1_embeddings, h)
        e2_h = tf.nn.embedding_lookup(self.ent2_embeddings, h)
        e1_t = tf.nn.embedding_lookup(self.ent1_embeddings, t)
        e2_t = tf.nn.embedding_lookup(self.ent2_embeddings, t)
        r1 = tf.nn.embedding_lookup(self.rel1_embeddings, r)
        r2 = tf.nn.embedding_lookup(self.rel2_embeddings, r)

        e_h = tf.complex(e1_h, e2_h)
        e_t = tf.complex(e1_t, e2_t)
        e_r = tf.complex(r1, r2)
        # Calculating score functions for all positive triples and negative triples
        res = tf.reduce_sum(self._calc(e_h, e_t, e_r), 1, keep_dims=False)
        if config.train_weighted:
            w = self.get_all_weights(in_batch=False)
            loss_func = tf.reduce_mean(tf.nn.softplus(- w * y * res), 0, keep_dims=False)
        else:
            loss_func = tf.reduce_mean(tf.nn.softplus(- y * res), 0, keep_dims=False)
        regul_func = tf.reduce_mean(e1_h ** 2) + tf.reduce_mean(e1_t ** 2) + tf.reduce_mean(e2_h ** 2) + tf.reduce_mean(
            e2_t ** 2) + tf.reduce_mean(r1 ** 2) + tf.reduce_mean(r2 ** 2)
        # Calculating loss to get what the framework will optimize
        self.loss = loss_func + config.lmbda * regul_func

    def predict_def(self):
        config = self.get_config()
        predict_h, predict_t, predict_r = self.get_predict_instance()
        predict_h_e1 = tf.nn.embedding_lookup(self.ent1_embeddings, predict_h)
        predict_t_e1 = tf.nn.embedding_lookup(self.ent1_embeddings, predict_t)
        predict_r_e1 = tf.nn.embedding_lookup(self.rel1_embeddings, predict_r)
        predict_h_e2 = tf.nn.embedding_lookup(self.ent2_embeddings, predict_h)
        predict_t_e2 = tf.nn.embedding_lookup(self.ent2_embeddings, predict_t)
        predict_r_e2 = tf.nn.embedding_lookup(self.rel2_embeddings, predict_r)

        predict_h_e = tf.complex(predict_h_e1, predict_h_e2)
        predict_t_e = tf.complex(predict_t_e1, predict_t_e2)
        predict_r_e = tf.complex(predict_r_e1, predict_r_e2)

        predict_r_e /= tf.norm(predict_r_e, 2, axis=1, keep_dims=True)

        self.predict = -tf.reduce_sum(self._calc(predict_h_e, predict_t_e, predict_r_e), 1, keep_dims=True)
