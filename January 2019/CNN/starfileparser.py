import pandas as pd


#general structure
GRDim =				'_rlnReferenceDimensionality'
GDDim =				'_rlnDataDimensionality'
GOImg =				'_rlnOriginalImageSize'
GCRes =				'_rlnCurrentResolution'
GCImg =				'_rlnCurrentImageSize'
GPF = 				'_rlnPaddingFactor'
GIH = 				'_rlnIsHelix'
GFSI = 				'_rlnFourierSpaceInterpolator'
GMRI = 				'_rlnMinRadiusNnInterpolation'
GPSz = 				'_rlnPixelSize'
GNrC = 				'_rlnNrClasses'
GNrB = 				'_rlnNrBodies'
GNrG = 				'_rlnNrGroups'
GT2FF = 			'_rlnTau2FudgeFactor'
GNCA = 				'_rlnNormCorrectionAverage'
GSO = 				'_rlnSigmaOffsets'
GOPM = 				'_rlnOrientationalPriorMode'
GSPRA = 			'_rlnSigmaPriorRotAngle'
GSPTA = 			'_rlnSigmaPriorTiltAngle'
GSPPA = 			'_rlnSigmaPriorPsiAngle'
GLH = 				'_rlnLog`hood'
GAP = 				'_rlnAveragePmax'

#classes structure
CRImg =				'_rlnReferenceImage'
CCD =				'_rlnClassDistribution'
CAR = 				'_rlnAccuracyRotations'
CAT = 				'_rlnAccuracyTranslations'
CER = 				'_rlnEstimatedResolution'
COFC =	 			'_rlnOverallFourierCompleteness'
CCPOX = 			'_rlnClassPriorOffsetX'
CCPOY =				'_rlnClassPriorOffsetY'

#Data model General Structure
dmg_labels = 		[GRDim, GDDim, GOImg,GCRes, GCImg, GPF, GIH, GFSI, GMRI, \
			 		 GPSz, GNrC, GNrB, GNrG, GT2FF, GNCA, GSO, GOPM, GSPRA, GSPTA, GSPPA, GLH, GAP]
#Data Model Classes Structure
dmc_labels = 		[CRImg, CCD, CAR, CAT, CER, COFC, CCPOX, CCPOY]
#Shorter version of Data Model Classes structure used in some jobs
sdmc_labels = 		[CRImg, CCD, CAR, CAT, CCPOX, CCPOY]

#metadata parameters
summary_labels = 	[
#					GRDim, GDDim, GOImg, \
#					GCRes, \
#					GCImg, GPF, GIH, GFSI, GMRI, \
					GPSz, \
#					GNrC, GNrB, GNrG, GT2FF, \
#					GNCA, GSO, \
#					GOPM, GSPRA, GSPTA, GSPPA, \
#					GLH, GAP, \
					CCD, CAR, CAT, \
#					CER, COFC, \
					CCPOX, CCPOY]

#define key strings to look for
dmgstr = 			'data_model_general'
dmcstr = 			'data_model_classes'	#general class
loopstr =			'loop_'
numclassesstr = 	'_rlnNrClasses'
numgroupsstr = 		'_rlnNrGroups'
dmscstr = 			'data_model_class_'	#specific class
dmgrstr = 			'data_model_groups'
selstr = 			'_rlnSelected'


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
	#now we have built the array (with values filled in) -- assign the names for the columns
	#values.columns = col_names;
	return (col_cnt, row_cnt)

def get_data_mode_classes(fp):

	dmc_array = []
	dmc_names = []
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
		(NrCol, NrRow) = get_loop_array(fp, dmc_names, dmc_array)
	return (NrCol, NrRow, dmc_array)


def get_data_mode_general(fp):

	dmg_array = []
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
		grow_rows(dmg_array, cnt, 2)
		#only 2 columns to be filled; so no fancy programming needed!
		dmg_array[cnt-1][0] = params[0]
		dmg_array[cnt-1][1] = float(params[1])
		if params[0] == numclassesstr:
			number_of_classes = params[1]
		if params[0] == numgroupsstr:
			number_of_groups = params[1]

	return (number_of_classes, number_of_groups, dmg_array)

def build_summary_table(i, dmc, dmg, summary_array):


	if len(dmc[i]) == len(dmc_labels):
		summary_array[i][summary_labels.index(CCD)] 	= dmc[i][dmc_labels.index(CCD)]
		summary_array[i][summary_labels.index(CAR)] 	= dmc[i][dmc_labels.index(CAR)]
		summary_array[i][summary_labels.index(CAT)]	 	= dmc[i][dmc_labels.index(CAT)]
		"""
		# should these be ignored or populated with an outlier value
		if dmc[i][dmc_labels.index(CER)] =='inf':
			#bad news: ML/TF would not understand "inf". Make it 10*min for the class? or 99
			summary_array[i][summary_labels.index(CER)] = 99
		else:
			summary_array[i][summary_labels.index(CER)] = dmc[i][dmc_labels.index(CER)]
		summary_array[i][summary_labels.index(COFC)] 	= dmc[i][dmc_labels.index(COFC)]
		"""
		summary_array[i][summary_labels.index(CCPOX)] 	= dmc[i][dmc_labels.index(CCPOX)]
		summary_array[i][summary_labels.index(CCPOY)] 	= dmc[i][dmc_labels.index(CCPOY)]

	#print (len(dmc[i]), len(sdmc_labels))
	if len(dmc[i]) == len(sdmc_labels):
		#print (i, dmc[i])
		summary_array[i][summary_labels.index(CCD)] 	= dmc[i][sdmc_labels.index(CCD)]
		summary_array[i][summary_labels.index(CAR)] 	= dmc[i][sdmc_labels.index(CAR)]
		summary_array[i][summary_labels.index(CAT)]	 	= dmc[i][sdmc_labels.index(CAT)]
		summary_array[i][summary_labels.index(CCPOX)] 	= dmc[i][sdmc_labels.index(CCPOX)]
		summary_array[i][summary_labels.index(CCPOY)] 	= dmc[i][sdmc_labels.index(CCPOY)]

	summary_array[i][summary_labels.index(GPSz)] 	= dmg[dmg_labels.index(GPSz)][1]
	"""
	#fill the general part of the arry
	summary_array[i][summary_labels.index(GOImg)] 	= dmg[dmg_labels.index(GOImg)][1]
	summary_array[i][summary_labels.index(GCRes)] 	= dmg[dmg_labels.index(GCRes)][1]
	summary_array[i][summary_labels.index(GCImg)] 	= dmg[dmg_labels.index(GCImg)][1]
	summary_array[i][summary_labels.index(GPF)] 	= dmg[dmg_labels.index(GPF)][1]
	summary_array[i][summary_labels.index(GFSI)] 	= dmg[dmg_labels.index(GFSI)][1]
	summary_array[i][summary_labels.index(GMRI)] 	= dmg[dmg_labels.index(GMRI)][1]
	summary_array[i][summary_labels.index(GT2FF)] 	= dmg[dmg_labels.index(GT2FF)][1]
	summary_array[i][summary_labels.index(GNCA)] 	= dmg[dmg_labels.index(GNCA)][1]
	summary_array[i][summary_labels.index(GSO)] 	= dmg[dmg_labels.index(GSO)][1]
	summary_array[i][summary_labels.index(GOPM)] 	= dmg[dmg_labels.index(GOPM)][1]
	summary_array[i][summary_labels.index(GSPRA)] 	= dmg[dmg_labels.index(GSPRA)][1]
	summary_array[i][summary_labels.index(GSPTA)] 	= dmg[dmg_labels.index(GSPTA)][1]
	summary_array[i][summary_labels.index(GSPPA)] 	= dmg[dmg_labels.index(GSPPA)][1]
	summary_array[i][summary_labels.index(GLH)] 	= dmg[dmg_labels.index(GLH)][1]
	summary_array[i][summary_labels.index(GAP)] 	= dmg[dmg_labels.index(GAP)][1]
	"""

def write_csv_output(col_names, value_matrix, csvfilepath):
	#let us write a csvfile too
	df = pd.DataFrame(value_matrix, columns= col_names)
	df.to_csv(csvfilepath)

def parse_model_and_create_csv(filepath, fp):
	dmg = []
	dmc = []

	for line in fp:
		# skip the blank lines
		# if line == "\n":
		# Empty line. Anything to be done?

		# get data mode general
		if dmgstr in line:
			# Data Model General block found
			(num_classes, num_groups, dmg) = get_data_mode_general(fp)
		# get data mode classes
		if dmcstr in line:
			# Data Model Classes block found
			(num_param_columns_found, num_classes_found,
			 dmc) = get_data_mode_classes(fp)
			if int(num_classes_found) == int(num_classes):
				# So far so good
				pass
			else:
				# we should never get here! Inconsistent/corrupted data set
				print(
					'we have a big problem: class number does not match!!')
				print(
					'number of classes found vs. real number of classes')
				print(num_classes_found, num_classes)

		# get data mode groups
		if dmgrstr in line:
			# group string found
			# this is used as a trigger for creating the csv file.  This needs to be changed and done at the end of file.
			summary_array = [[0 for j in range(len(summary_labels))] for
							 i in range(int(num_classes))]
			summary_names = [[] for i in
							 range(int(len(summary_labels)))]
			# compute the averages as needed and fill the array one row at a time
			i = 0

			while i < int(num_classes):
				build_summary_table(i, dmc, dmg, summary_array)
				i += 1
			# record the data in a file with .xls extension
			csvfilepath = filepath.replace(".star", ".csv")
			# enable it after debug
			write_csv_output(summary_labels, summary_array, csvfilepath)

			break


def parse_selection_and_create_csv(filepath, fp):

	NrCol = 0
	NrRow = 0
	sel_names = []
	sel = []

	#skip the next line if blank
	line = next(fp)
	while line == "\n" or line =='data_\n' or 'RELION' in line:
		#print('::GDMC EMPTY LINE::')
		line = next(fp)
	#line = next(fp)		#why is this needed

	# see if loop_ is there
	if loopstr in line:
		#print("::GDMC LOOP FOUND::")
		(NrCol, NrRow) = get_loop_array(fp, sel_names, sel)
		#print (NrCol, NrRow, sel)

	csvfilepath = filepath.replace(".star", ".csv")
	write_csv_output(sel_names, sel, csvfilepath)

	return (NrCol, NrRow)
