from keras.preprocessing.image import ImageDataGenerator, img_to_array
import cv2
import os
import glob
from urllib.parse import unquote
from os.path import basename
from constants import IMAGE_SIZE, TRAIN_DATA_PATH, IMAGE_AUG_SUBDIR


datagen = ImageDataGenerator(
        rotation_range=40,
        width_shift_range=1,
        height_shift_range=1,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest')


def duplicate(source):

	pics = glob.glob(source+'/'+'*.png')
	image_size = IMAGE_SIZE

	i=0

	for pic in pics:

		#read an image
		img = cv2.imread(pic,0)
		#get it ready for randomization
		img = cv2.resize(img,(image_size,image_size))
		x = img_to_array(img)
		x = x.reshape((1,) + x.shape)
		i = i+1

		# ref: https://stackoverflow.com/questions/14511435/python-getting-filename-from-long-path
		prefix = basename(unquote(pic)).replace('.png','')
		if IMAGE_AUG_SUBDIR == '':
			destination = source
		else:
			destination=source + IMAGE_AUG_SUBDIR

		#filepath.replace(".star",".csv")
		# the .flow() command below generates batches of randomly transformed images
		# and saves the results to the `preview/` directory
		# ref: https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html
		j = 0
		for batch in datagen.flow(x, batch_size=1,
                          save_to_dir= destination, save_prefix=prefix, save_format='png'):
			j += 1
			if j > 10:
	 	       		break

def dupimages():
	rootpath = TRAIN_DATA_PATH
	rootDir = os.getcwd() + '/' + rootpath
	for dirName, subdirList, fileList in os.walk(rootDir):
		for subdir in subdirList:
			duplicate (dirName+'/'+subdir)

if __name__ == '__main__':
	dupimages()




