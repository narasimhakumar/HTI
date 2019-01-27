from __future__ import division, print_function, absolute_import
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.layers.merge_ops import merge
import cv2
import os
from pathlib import Path
import pandas as pd
import numpy as np
from constants import IMAGE_SIZE, TEST_DATA_PATH, STATUS_FILE_NAME, CNN_SAVED_FILE, ENABLE_METADADA
from common import summary_labels, GPSz


def identify():

    #Creating and loading trained model
    #---------------------------------------------------------
    network = input_data(shape=[None, IMAGE_SIZE, IMAGE_SIZE, 1])
    # change the 9 to something valid!!!!
    mdnetwork = input_data(shape=[None, 6])

    network = conv_2d(network, 30, 3, activation='relu')
    network = max_pool_2d(network, 2)
    network = conv_2d(network, 30, 3, activation='relu')
    network = max_pool_2d(network, 2)
    network = conv_2d(network, 40, 3, activation='relu')
    network = conv_2d(network, 40, 3, activation='relu')
    network = max_pool_2d(network, 2)
    network = conv_2d(network, 40, 3, activation='relu')
    network = conv_2d(network, 30, 3, activation='relu')
    network = fully_connected(network, 100, activation='relu')

    if ENABLE_METADADA:
        network = merge([network,mdnetwork], 'concat')

    network = dropout(network, 0.5)
    network = fully_connected(network, 50, activation='relu')
    network = fully_connected(network, 2, activation='softmax')
    network = regression(network)
    model = tflearn.DNN(network)
    model.load(CNN_SAVED_FILE)

    #-------------------------------------------------------
    #go thru test images in test image directory

    rootpath = TEST_DATA_PATH
    rootDir = os.getcwd() + '/' + rootpath
    home = str(Path.home())
    for dirName, subdirList, fileList in os.walk(rootDir):
        # read the metadata model file
        # csv file is dirname + job+ '-model.csv'
        if TEST_DATA_PATH +'/job' in dirName:
            csv_fname = os.path.basename(dirName)+'-model.csv'
            metadata_fname = dirName + '/' + csv_fname
            print (metadata_fname)
            if os.path.isfile(metadata_fname):
                #get the metadata, even if it is not used later
                metadata = pd.read_csv(metadata_fname, sep=',')
                metadata = metadata.drop(metadata.columns[0], axis=1)
                metadata = metadata.as_matrix()
                metadata_size = np.size(metadata, 1)

        status_fname = dirName[dirName.find(rootpath):]+'/'+ STATUS_FILE_NAME
        status_f = open(status_fname, 'w')
        for fname in fileList:
            if 'png' in fname:
                image_fname = dirName + '/' + fname
                # predict and write the result
                img = cv2.imread(image_fname, 0)
                orig_img_len = np.size(img, 0)  # rows and colums should be the same
                img = cv2.resize(img, (IMAGE_SIZE,IMAGE_SIZE), interpolation=cv2.INTER_AREA)
                resized_img_len = np.size(img, 0)
                img = img.reshape([-1, IMAGE_SIZE, IMAGE_SIZE, 1])
                #img = np.reshape(img, (-1, 64, 64, 1))
                # get metadata
                start = fname.find('-classes-') + len('-classes-')
                end = fname.find('.png')
                #class_num = int(fname[start:start + 3:])
                class_num = int(fname[start:end:])
                #print (class_num)
                if resized_img_len != orig_img_len:
                    metadata[class_num - 1][summary_labels.index(GPSz)] = \
                        metadata[class_num - 1][summary_labels.index(
                            GPSz)] * orig_img_len / resized_img_len
                else:
                    pass
                Z = metadata[class_num - 1]

                if ENABLE_METADADA:
                    pre = model.predict([img, np.array(Z).reshape(-1, metadata_size)])
                else:
                    pre = model.predict(img)

                if pre[0][0] >= 0.5:
                    print("%s,1" % fname, file=status_f)
                elif pre[0][1] >= 0.5:
                    print("%s,0" % fname, file=status_f)
                else:
                    print("%s,255" %fname, file=status_f)

        status_f.close()


if __name__ == '__main__':
	identify()