import cv2
import numpy as np
import glob
import pickle
import pandas as pd


# For accepted [1,0]
# For rejected [0,1]

"""
Get the filename in the trainaing directory
extract the job and class nummber
get the selection data (accepted vs. rejected) from the selection csv
get the metadata from the model csv
combine bitmap, selection and metadata into that structure
create the data file
"""

def create_data(job, train, file):

    #build the job and selection file name
    model_filename = train+'/'+job+'_model.csv'
    selection_filename= train+'/'+job+'_selection.csv'

    #cache the data from those files
    metadata = pd.read_csv(model_filename, sep=',')
    metadata = metadata.drop(['Class'], 1)
    metadata = metadata.as_matrix()
    # selection is not a csv file. just a text file
    selection = np.loadtxt(selection_filename)

    image_size = 64
    length = image_size * image_size

    pics = glob.glob(train+'/'+job+'*.png')
    total_images = len(pics)

    array_size = length +2 + metadata.shape[1]
    main_data = np.zeros([total_images, array_size], dtype='f')

    #read images and fill the databuffer
    i = 0
    for pic in pics:
        img = cv2.imread(pic, 0)
        img = cv2.resize(img, (image_size, image_size))
        main_data[i, 0:length] = np.reshape(img, (1, length))
        # find the class

        start = pic.find('_classes-') + len('_classes-')
        class_num = int(pic[start:start+2:])

        if selection[class_num-1] == 1:
            #accepted
            main_data[i, length] = 1
        else:
            if selection[class_num-1] == 0:
                #rejected
                main_data[i, length + 1] = 1
            else:
                print ('Houston, we have a problem!!!')

        #stuff meta data
        main_data[i, length+2:] = metadata [class_num-1]
        i = i + 1

    np.random.shuffle(main_data)
    pickle.dump (main_data, file)
    return

#zap existing files
file = open('main_data.p', 'wb')
file.close()

job_list = ['job011', 'job013', 'job019']
destination = 'data/train'
for i, job in enumerate(job_list):
    file = open('main_data.p', 'ab')
    create_data(job, destination, file)
    file.close()

