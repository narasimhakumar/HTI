from __future__ import division, print_function, absolute_import
import numpy as np
import tflearn
from tflearn.data_utils import shuffle, to_categorical
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.layers.merge_ops import merge
import cv2
import os
import glob
import pandas as pd
import numpy as np

path = 'data/test'
#read the metadata model file
metadata = pd.read_csv('data/test/job027_model.csv', sep=',')
# print (metadata)
metadata = metadata.drop(['Class'], 1)
metadata = metadata.as_matrix()

#Creating and loading trained model
#---------------------------------------------------------
network = input_data(shape=[None, 64, 64, 1])
mdnetwork = input_data(shape=[None, 9])

network = conv_2d(network, 30, 3, activation='relu')
network = max_pool_2d(network, 2)
network = conv_2d(network, 30, 3, activation='relu')
network = max_pool_2d(network, 2)
network = conv_2d(network, 40, 3, activation='relu')
#network = max_pool_2d(network, 2)
network = conv_2d(network, 40, 3, activation='relu')
network = max_pool_2d(network, 2)
network = conv_2d(network, 40, 3, activation='relu')
#network = max_pool_2d(network, 2)
network = conv_2d(network, 30, 3, activation='relu')
#network = max_pool_2d(network, 2)
network = fully_connected(network, 100, activation='relu')
network = merge([network,mdnetwork], 'concat')
network = dropout(network, 0.5)
network = fully_connected(network, 50, activation='relu')
network = fully_connected(network, 2, activation='softmax')
network = regression(network)
model = tflearn.DNN(network)
model.load('my_cnn.tflearn')

#-------------------------------------------------------
#go thru test images in test image directory

f = open('results.txt', 'w')
for filename in glob.glob(os.path.join(path, '*.png')):

	img = cv2.imread(filename,0)
	# Making prediction
	img = np.reshape(img,(-1,64,64,1))
	#get metadata
	start = filename.find('_classes-') + len('_classes-')
	class_num = int(filename[start:start + 3:])
	Z = metadata [class_num-1]

	pre = model.predict([img, np.array(Z).reshape(-1, 9)])
	if pre[0][0] >= 0.5:
		print("%s,1"%filename, file=f)
	elif pre[0][1] >= 0.5:
		print("%s,0"%filename, file=f)
	else:
		print("%s,255"%filename, file=f)

f.close()