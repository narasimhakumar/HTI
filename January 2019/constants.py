PI = 3.14

"""
These parameters will eventually be setup via the UI
"""

"""
Basic config parameters
"""
IMAGE_SIZE =            32      #size of the images.  Prefer to match the smallest size so no image has to be stretched
IMAGE_AUGMENTATION =    False   #Image augmentation with many images flag
DIRECT_IMAGE_EXTRACT =  False   #png creation flag; if true, no pngs will be created

ENABLE_METADADA =       True    # To or not to use Metadata (in the model.star file).
NORMALIZE =             False   # Metadata to be normalized
NORMALIZE_MAX_TO_1 =    False   # Set the normalization so data is between 1 and 0
NORMALIZE_MEAN_TO_1 =   False   # set the normalization so mean is 1

"""
Path names for data and results files and folders
"""
TRAIN_DATA_PATH =       'data/train-1'
TRAIN_DATA_FILE =       'train_data.p'
TEST_DATA_PATH  =       'data/test-1'
STATUS_FILE_NAME =      'status.txt'
OHSU_TRAINING_FILES_PATH = 'Documents/OHSU-data-Nov-20-2018/training-1'
OHSU_TEST_FILES_PATH =  'Documents/OHSU-data-Nov-20-2018/training-2'
E2PROC2D_PATH =         'EMAN2/bin/e2proc2d.py'     #tool to expand mrcs files into png pictures
OVERALL_RESULTS =       'overall_results.csv'
IMAGE_AUG_SUBDIR =      ''                          #only null supported now

CNN  =                  'my_cnn'
CNN_SAVED_FILE =        'my_cnn.tflearn'

BATCH_SIZE =            96
EPOCH =                 20
VALIDATION_SET =        0.1
SHOW_METRIC =           True



