
import sys
import os
import csv
import operator
import numpy as np
from constants import TEST_DATA_PATH, STATUS_FILE_NAME, OVERALL_RESULTS

overall_results = []

def update_results(sel, sorted_stat, job):

	#create the current job results file
	current_job_results = []

	if sorted_stat == 0:
		#write zeros in overall results
		return

	false_pos = 0
	false_neg = 0
	correct_prediction = 0
	incorrect_prediction = 0

	i = 0
	for row in sel:
		if 'Selected' in row[1]:
			#ignore 1st row
			print ('empty first row: %s'%row[1])
		else:
			#print (row[0], row[1], sorted_stat[i-1][0], sorted_stat[i-1][1])
			if row[1] == sorted_stat[i-1][1]:
				correct_prediction +=1
				current_job_results.append([job, row[0], row[1], sorted_stat[i-1][1],0, 0])
			else:
				incorrect_prediction += 1
				if row[1] > sorted_stat[i-1][1]:
					false_neg += 1
					current_job_results.append([job, row[0], row[1], sorted_stat[i - 1][1], 0, 1])
				else:
					false_pos += 1
					current_job_results.append([job, row[0], row[1], sorted_stat[i - 1][1], 1, 0])
		i += 1

	#overall_results.append(['job'+str(job), ])
	overall_results.append([job, i-1, correct_prediction, incorrect_prediction, false_pos, false_neg, (correct_prediction/(i-1))])
	print (overall_results)


def verify_results():

	rootpath = TEST_DATA_PATH
	if not os.path.exists(rootpath):
		print('File path {} does not exist. Exiting...'.format(rootpath))
		sys.exit()

	rootDir = os.getcwd() + '/' + rootpath
	for dirName, subdirList, fileList in os.walk(rootDir):
		for fname in fileList:
			filepath = dirName+'/'+fname
			if 'selection.csv' in fname:
				#read selection.csv
				sel_f = open(filepath, 'rt')
				sel = csv.reader(sel_f)
				#read status.txt
				stat_filepath = dirName +'/' + STATUS_FILE_NAME
				job_name = fname[:fname.find('-selection.csv')]
				job = int(job_name[job_name.find('job')+3:])
				#print (job_name, job)
				if os.path.isfile(stat_filepath) and os.path.getsize(stat_filepath) > 0:
					stat_f = open (stat_filepath, 'rt')
					stat = csv.reader(stat_f)
					# sort status.txt
					sorted_stat = sorted(stat, key=operator.itemgetter(0))
					update_results(sel, sorted_stat, job)
					# generate the results file for that job & generate the global stats for that job and append to the global results
					# write results.csv for that job
				else:
					#the status file doesnt exist
					#update the global status with zeros
					overall_results.append([job, 0, 0, 0, 0, 0, 0])
					print ('%s is either missing or zero'%stat_filepath)
					pass
				#break
				pass

	np.savetxt(OVERALL_RESULTS, overall_results, \
	#			header = 'Job, Num_Classes, Correct_Prediction, Incorrect_Prediction, False_Pos, False_Neg, Prediction_percentage', \
				delimiter =',')


if __name__ == '__main__':
	verify_results()
