# Import the os module, for the os.walk function
import os
from pathlib import Path
from constants import OHSU_TRAINING_FILES_PATH, OHSU_TEST_FILES_PATH, TRAIN_DATA_PATH, TEST_DATA_PATH

def CreateDirAndCopy(rootDir, datapath):
    for dirName, subdirList, fileList in os.walk(rootDir):
        if 'ex-' in dirName:
            dirnameonly = dirName[dirName.find('ex-')+3:]
            os.system('mkdir '+ datapath +'/'+'job'+dirnameonly)
        for fname in fileList:
            filename = 'job'+dirnameonly+'-'+fname
            cps = 'cp '+dirName+'/'+fname+' '+ datapath +' /job'+dirnameonly+ '/'+filename
            os.system(cps)

def cpfiles():
    # Set the directory you want to start from
    home= str(Path.home())
    #Training data
    rootDir = home+'/'+ OHSU_TRAINING_FILES_PATH
    CreateDirAndCopy(rootDir, TRAIN_DATA_PATH)
    #Test data
    rootDir = rootDir = home+'/'+ OHSU_TEST_FILES_PATH
    CreateDirAndCopy(rootDir, TEST_DATA_PATH)

if __name__ == '__main__':
	cpfiles()





