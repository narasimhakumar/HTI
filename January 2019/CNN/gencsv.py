import sys
import os
from starfileparser import parse_model_and_create_csv, parse_selection_and_create_csv
from constants import TRAIN_DATA_PATH, TEST_DATA_PATH

def gen_csv(rootpath):

	if not os.path.exists(rootpath):
		print('File path {} does not exist. Exiting...'.format(rootpath))
		sys.exit()

	rootDir = os.getcwd() + '/' + rootpath
	for dirName, subdirList, fileList in os.walk(rootDir):
		for fname in fileList:
			filepath = dirName+'/'+fname
			if 'model.star' in filepath:
				#print (filepath)
				parse_model_and_create_csv(filepath, open(filepath))
				#pass
			if 'selection.star' in filepath:
				#print (filepath)
				parse_selection_and_create_csv(filepath, open(filepath))

def main():
	#first create training csv files and then the test csv files
	#training csv
	gen_csv(TRAIN_DATA_PATH)
	#test csv
	gen_csv(TEST_DATA_PATH)


if __name__ == '__main__':  
	main()
