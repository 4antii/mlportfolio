import tensorflow as tf
import os
import numpy as np
import time as time
from scipy.io.wavfile import write 
import uuid
#import tensorflow.compat.v1 as tf
#tf.disable_v2_behavior()

def generate(drum, part, interpolation):
    if(drum == 'snare'):
        dirrInfer = './checkpoints/snare/infer/infer.meta'
        dirrCheck =  './checkpoints/snare/model.ckpt-6810'
    if(drum == 'kick'):
        dirrInfer = './checkpoints/kick/infer/infer.meta'
        dirrCheck =  './checkpoints/kick/model.ckpt-50037'
    if(drum == 'hh'): 
        dirrInfer = './checkpoints/hh/infer/infer.meta'
        dirrCheck =  './checkpoints/hh/model.ckpt-5753'
    if(drum == 'clap'): 
        dirrInfer = './checkpoints/clap/infer/infer.meta'
        dirrCheck =  './checkpoints/clap/model.ckpt-10544'
    tf.reset_default_graph()
    saver = tf.train.import_meta_graph(dirrInfer)
    graph = tf.get_default_graph()
    sess = tf.InteractiveSession()
    saver.restore(sess, dirrCheck)
    # Sample latent vectors
    _z = (np.random.rand(1, 100) * 2.) - 1.
    # Generate
    z = graph.get_tensor_by_name('z:0')
    G_z = graph.get_tensor_by_name('G_z:0')[:, :, 0]
    _G_z = sess.run(G_z, {z: _z})
    filename = str(uuid.uuid4().hex)[:10]
    path = './sounds/'+ filename + ".wav"
    write(path, 41100, _G_z[0])
    if(drum == 'kick' and part == 'hi'):
        return write(path, 41100, _G_z[0])
    return filename + ".wav"
    





