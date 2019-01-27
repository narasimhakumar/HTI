# Import the os module, for the os.walk function
import os
from pathlib import Path
from constants import OHSU_TEST_FILES_PATH, TEST_DATA_PATH
 
# Set the directory you want to start from

home= str(Path.home())
rootDir = home+'/'+ OHSU_TEST_FILES_PATH
for dirName, subdirList, fileList in os.walk(rootDir):
    if 'ex-' in dirName:
        dirnameonly = dirName[dirName.find('ex-')+3:]
        os.system('mkdir '+ TEST_DATA_PATH + '/'+'job'+dirnameonly)
    for fname in fileList:
        filename = 'job'+dirnameonly+'-'+fname
        cps = 'cp '+dirName+'/'+fname+' '+ TEST_DATA_PATH +'/job'+dirnameonly+ '/'+filename
        os.system(cps)





