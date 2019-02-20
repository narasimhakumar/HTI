
import sys
import os
import pandas as pd
from pathlib import Path
from constants import E2PROC2D_PATH, TRAIN_DATA_PATH, TEST_DATA_PATH

def create_pngs (e2proc2d_path, mrcs_filepath, png_filepath):
    print (e2proc2d_path, mrcs_filepath, png_filepath+'.png')
    command_str = e2proc2d_path +' ' + mrcs_filepath + ' '+ png_filepath+'.png' + ' --unstacking --writejunk'
    os.system(command_str)

def traverse_and_create(e2proc2d_path, rootDir):
    for dirName, subdirList, fileList in os.walk(rootDir):
        for fname in fileList:
            mrcs_filepath = dirName + '/' + fname
            png_filepath = dirName + '/' + fname.replace('.mrcs', '')
            if 'mrcs' in mrcs_filepath:
                create_pngs(e2proc2d_path, mrcs_filepath, png_filepath)

def genpngs():
    home = str(Path.home())
    e2proc2d = home + '/' + E2PROC2D_PATH
    #create training pngs
    rootDir = os.getcwd() + '/' + TRAIN_DATA_PATH
    traverse_and_create (e2proc2d, rootDir)
    #create test pngs
    rootDir = os.getcwd() + '/' + TEST_DATA_PATH
    traverse_and_create (e2proc2d, rootDir)


if __name__ == '__main__':
	genpngs()
