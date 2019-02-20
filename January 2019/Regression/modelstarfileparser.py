"""

	Relion format model star file parser and analyzer
	Narasimha Kumar
	Oct 2018

	Reads the *model*.star file in this order

	1) General Data listed in "data_model_general": In addition to reading and storing
		parameters number of classes and groups are stored and later used for
		further data creation
	2) Classes data (common for all classes) listed in "data_model_classes": The number
		of classes (i.e. rows) should match the number of classes obtained in
		the previous step
	3) Specific class data listed under "data_model_class_i" (i being the index 1 thru
		number of classes)

	Key Python challenges solved (may not be efficient)
	a) dynamic arrays creation: allocation arrays based on the number of classes (and
		groups) at runtime. It would be an array of arrays,1D array of 2D or 1D arrays
	b) dynamic arrays expansion: expanding the arrays as more data is read into
		(expansion of rows)



"""

import sys  
import os
import pandas as pd
import numpy as np
import statistics as s
import xlwt
from xlwt import Workbook


#define key strings to look for
dmgstr = 'data_model_general'
dmcstr = 'data_model_classes'	#general class
loopstr = 'loop_'
numclassesstr = '_rlnNrClasses'
numgroupsstr = '_rlnNrGroups'
dmscstr = 'data_model_class_'	#specific class
dmgrstr = 'data_model_groups'    


#define the data model general and data model classes array
dmg=[]		#general array -- 2 column?
dmc=[]		#classes array (2d matrix)
dmc_names=[]	#names for classes array columns
#dmcn_names=[]	#arrary of n class (1D) array of names
temp_array=[]
temp_names=[]


def grow_rows(arr, row_cnt, col_cnt):
	missing = row_cnt - len(arr)
	if missing > 0:
		arr.extend([[0] * col_cnt for i in range(missing)])

def get_loop_array(fp, col_names, values):

	#first get the column names, and count and then get the data (2D array)
	#column names would end when the line does not start with "_"

	col_cnt=0
	row_cnt=0
	for line in fp:	
		if line[0] == "_":
			#we have a label
			params = line.split()
			col_names.append(str(params[0])) 
			col_cnt += 1
		else:
			break

	#now we know the columns, names
	#we may not know the number of rows
	#read until the next blank line

	while line != "\n":	
		
		#get parameters (col_cnt number of parameters)
		params = line.split()
		if len(params) == 0:
			#why did we get here? \n should have caught the blank line.  maybe spaces?
			break
		
		row_cnt += 1	

		i=0

		#get a new row of col_cnt columns
		grow_rows(values, row_cnt, col_cnt)

		#fill the rows
		while i < col_cnt:
			values[row_cnt-1][i] = params[i]
			i +=1
		line = next(fp)

	#now we have built the 2D array (with values filled in) -- assign the names for the columns
	#values.columns = col_names;

	return (col_cnt, row_cnt)

def get_data_mode_classes(fp):

	NrCol = 0
	NrRow = 0	

	#skip the next line if blank
	line = next(fp)
	if line == "\n":
		#print('::GDMC EMPTY LINE::')
		pass
	line = next(fp)		#why is this needed

	# see if loop_ is there
	if loopstr in line:
		#print("::GDMC LOOP FOUND::")
		(NrCol, NrRow) = get_loop_array(fp, dmc_names, dmc)
	return (NrCol, NrRow)

def get_data_mode_class_i(fp, cnt):

	NrCol = 0
	NrRow = 0
	temp_array = []

	#skip the next line if blank
	line = next(fp)
	if line == "\n":
		#print('::GDMCI EMPTY LINE::')
		pass

	line = next(fp)	# need to explain why this

	# see if loop_ is there
	if loopstr in line:
		#print("::GDMCI LOOP FOUND:: Class i %d"%cnt)
		(NrCol, NrRow) = get_loop_array(fp, temp_names, temp_array)
	return (NrCol, NrRow, temp_array, temp_names)

def get_data_mode_general(fp):

	number_of_classes = 0
	number_of_groups = 0

	#skip the next line if blank
	line = next(fp)
	if line == "\n":
		#print('::EMPTY LINE::')
		pass

	#read the str and values for everyline  until a blank line found
	#find the number of classes and groups by looking for the key string match
	cnt = 0		
	for line in fp:			
		if line == "\n" or len(line.strip()) == 0:
			#print("::EMPTY LINE:: Reached the end!!")
			#print DataFrame(dmg)
			break			
		cnt += 1
		params = line.split()
		grow_rows(dmg, cnt, 2)
		
		#only 2 columns to be filled; so no fancy programming needed!
		dmg[cnt-1][0] = params[0]
		dmg[cnt-1][1] = float(params[1])

		if params[0] == numclassesstr:
			number_of_classes = params[1]			
		if params[0] == numgroupsstr:
			number_of_groups = params[1]

	return (number_of_classes, number_of_groups)

def write_csv_output(col_names, value_matrix, csvfilepath):

	#excel sheet for export to others
	#wb = Workbook()
	#sheet = wb.add_sheet('Data Model Classes')
	
	#write columns
	#i=0
	#while i < int(num_cols):
	#	sheet.write(0, i+1, col_names[i])
	#	i+=1

	#write rows
	#i=0
	#while i< int(num_rows):
	#	s = 'Class' + str(i+1)
	#	sheet.write(i+1, 0, s)
	#	i+=1

	#fill the cells
	#i=0
	#while i < int(num_rows):
	#	j=0
	#	while j < int(num_cols):
	#		sheet.write(i+1, j+1, value_matrix[i][j])
	#		j+=1
	#	i+=1

	#print ('writing an excel file')
	#wb.save(excelfilepath)

	#let us write a csvfile too
	df = pd.DataFrame(value_matrix, columns= col_names)
	df.to_csv(csvfilepath)

def build_summary_table(i, dmc, data_class_data, summary_array):

	#fill the easy parts first: copy cells from Data Model Classes array
	summary_array[i][0] = dmc[i][2]	# Accuracy Rotations
	summary_array[i][1] = dmc[i][3]	# Accuracy Translations
	summary_array[i][2] = dmc[i][4]	# Estimated Resolution
	summary_array[i][6] = dmc[i][5]	# Accuracy Translations

	#now comes the hard part. 
	#	find averages for each of the pamaters for each class

	#dimensions of the summary matrix to be created
	#	this could be outside the loop, unless arrays are of different sizes
	data_class_data_rows = len(data_class_data[i])
	data_class_data_cols = len(data_class_data[i][0])
	#create the array: This could be done outside the loop.
	array_i = [[0 for x in range(int(data_class_data_cols))] \
		for y in range(int(data_class_data_rows))]
	#fill the array with data found scanning the star file
	array_i = data_class_data[i]

	#copy the column of interest to a linear array:
	#	should be a better way to slice the 2D arrays

	test_array = [[] for x in range(int(data_class_data_rows))]

	# Average Ssnr Map
	j=0
	while j < int(data_class_data_rows):
		test_array[j] = float(array_i[j][3])
		j+=1
	mean = s.mean(test_array)
	summary_array[i][3] = mean
	#print("SSNR Map mean %f"%mean)

	# Average Ref Sigma 2
	j=0
	while j < int(data_class_data_rows):
		test_array[j] = float(array_i[j][6])
		j+=1
	mean = s.mean(test_array)
	summary_array[i][4] = mean
	#print("Sigma 2 mean %f"%mean)

	# Average Spectral Orientability Contribution
	# Unlike other fields, this may not exist for some classes. Write a zero for those.
	j=0
	while j < int(data_class_data_rows):
		#existence check by a colum check
		if len(array_i[0]) == 9:
			test_array[j] = float(array_i[j][8])
		else:
			test_array[j]=0
		j+=1
	mean = s.mean(test_array)
	summary_array[i][5] = mean
	#print("SOC mean %f"%mean)

	# Average Average Fourier Completeness
	j=0
	while j < int(data_class_data_rows):
		test_array[j] = float(array_i[j][5])
		j+=1
	mean = s.mean(test_array)
	summary_array[i][7] = mean
	#print("Fourier mean %f"%mean)

	# Average Average Reference Tau2
	j=0
	while j < int(data_class_data_rows):
		test_array[j] = float(array_i[j][7])
		j+=1
	mean = s.mean(test_array)
	summary_array[i][8] = mean
	#print("Tau2 mean %f"%mean)

	#make the prediction
	# if the overall Fourier is 1, average Fourier is > 0.7 (later: ,and average tau2 <0.0005) then good
	#if float(summary_array[i][6]) == 1 and float(summary_array[i][7]) > 0.7:
	#	summary_array[i][9]=1
	#else:
	#	summary_array[i][9]=0


def main():  

	filepath = sys.argv[1]

	num_classes_found = 0
	num_param_columns_found = 0;
	num_classes=0
	num_groups=0
	class_count=0
	col=0
	row=0

	print('filepath %s'%filepath)

	if not os.path.isfile(filepath):
		print('File path {} does not exist. Exiting...'.format(filepath))
		sys.exit()


	with open(filepath) as fp:
		for line in fp:
			# skip the blank lines
			#if line == "\n":
				# Empty line. Anything to be done?
			
			#get data mode general
			if dmgstr in line:
				# Data Model General block found
				(num_classes, num_groups) = get_data_mode_general (fp)
			
			#get data mode classes
			if dmcstr in line:
				# Data Model Classes block found
				(num_param_columns_found, num_classes_found) =  get_data_mode_classes (fp)
				if int(num_classes_found) == int(num_classes):
					# So far so good
					# create arrays to capture each class data and column names
					data_class_data = [[] for i in range(int(num_classes))]
					data_class_names = [[] for i in range(int(num_classes))]
	
				else:
					# we should never get here! Inconsistent/corrupted data set
					print ('we have a big problem: class number does not match!!')
					print ('number of classes found vs. real number of classes')
					print (num_classes_found, num_classes)
					#break

			#now get individual class details for each class

			if (line.find(dmscstr,0) != -1):
				#print ("DM Class structure found for %d"%class_count)
				(col, row, data_class_data[class_count],data_class_names[class_count])=get_data_mode_class_i(fp, class_count)
				class_count += 1
				line = next(fp)
			else:
				#print ('string not found')
				#print (line)
				pass


			#get data mode groups
			if dmgrstr in line:
				#group string found

				#   A N A L Y S I S ----  P R E P A R A T I O N
				# Caution: ::REAL BAD PROGRAMMING BELOW ::
				#	Quick and Dirty Method followed, as the analysis is not perfect
				#
				# Create the Summary Matrix, to be ready for Analysis
				# Need a separate routine when more general formualas, and no embedded constants
				#
				# The summary matrix will have these columns:
				#	 . Class Number??? -- let us not include now, as it is just the row number
				#	1. Accuracy Rotations
				#	2. Accuracy Translations
				#	3. Estimated Resolution
				#	4. Average SSNR map
				#	5. Average Sigma2
				#	6. Average SprectralOrientabilityContribution
				#	7. Overall Fourier Completeness
				#	8. Average Fourier Completeness
				#	9. Average Reference Tau2
				#	10.Prediction
				#
				#	"Average" is average across each class data
				#
				# Implementation
				#	1. Create 2 arrays: one for data and another for column names:
				#		Data array: Rows: # of classes; Columns: 10(above properties)
				#	2. Compute the values for each row and fill the array row:
				#		use stats primitives for average
				#	3. Extend the array by a row, and repeat (2) until all rows are filled.
				#
				# create the 2D array, with column number from above, and row numer=number of classes
				#	change if more variables or stat ops are needed accordingly
				col = 9
				summary_array = [[0 for j in range(col)] for i in range(int(num_classes))]
				summary_names = [[] for i in range(int(col))]

				#set the names first
				summary_names= ["_rlnAccuracyRotations", \
					"_rlnAccuracyTranslations", \
					"_rlnEstimatedResolution", \
					"Average SSNR Map", \
					"Average Reference Sigma2", \
					"Average SpectOriContrib", \
					"_rlnOverallFourierCompleteness", \
					"Average Fourier Completeness", \
					"Average Reference Tau2"]


				# compute the averages as needed and fill the array one row at a time
				i = 0
				print (num_classes)
				while i<int(num_classes):
					build_summary_table(i, dmc, data_class_data, summary_array)
					i+=1

				#record the data in a file with .xls extension
				csvfilepath = filepath.replace(".star",".csv")
				write_csv_output(summary_names, summary_array, csvfilepath)


				print("%s is found"%(dmgrstr))
				break

if __name__ == '__main__':  
	main()

