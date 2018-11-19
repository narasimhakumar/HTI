from __future__ import division, print_function, absolute_import
import numpy as np
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.layers.merge_ops import merge
import pickle
import dask.array as da

# Data loading and preprocessing
#this is a nightmare since pickle load might have been done multiple times,
# and each load provides a chunk
# dask comes to the rescue!

f = open('main_data.p', 'rb')

train_data = pickle.load(f)
while 1:
        try:
            train_data1 = pickle.load(f)
            data = [train_data, train_data1]
            train_data = da.concatenate(data, axis=0)
        except EOFError:
            break

#extract pictures (0 thru 4095), next two bytes for the selection, and the rest for metadata
X, Y, Z  = train_data[:,0:4096],train_data[:,4096:4098], train_data[:,4098:]
X = X.reshape([-1,64,64,1])

network = input_data(shape=[None, 64, 64, 1])
mdnetwork = input_data(shape=[None, 9])
network = conv_2d(network, 30, 3, activation='relu')
network = max_pool_2d(network, 2)
network = conv_2d(network, 30, 3, activation='relu')
#network = max_pool_2d(network, 2)
network = conv_2d(network, 40, 3, activation='relu')
network = max_pool_2d(network, 2)
network = conv_2d(network, 40, 3, activation='relu')
#network = max_pool_2d(network, 2)
network = conv_2d(network, 40, 3, activation='relu')
#network = max_pool_2d(network, 2)
network = conv_2d(network, 30, 3, activation='relu')
network = max_pool_2d(network, 2)
network = fully_connected(network, 100, activation='relu')

network = merge([network,mdnetwork], 'concat')

network = dropout(network, 0.5)
network = fully_connected(network, 50, activation='relu')
network = fully_connected(network, 2, activation='softmax')

# Train using classifier
network = regression(network, optimizer='adam',
                     loss='categorical_crossentropy',
                     learning_rate=0.001)

model = tflearn.DNN(network, tensorboard_verbose=3)
model.fit([np.array(X).reshape(-1, 64, 64, 1), np.array(Z).reshape(-1, 9)], Y, n_epoch=20, shuffle=True, validation_set=0,
        show_metric=True, batch_size=96, run_id='my_cnn')


model.save('my_cnn.tflearn')
