
import os
import glob


Imagefilepath_index=5


starfile_startsearch = "/home/nkumar/Documents/OHSU-data-May-22-2019"

def extract_mrcsfile(line):
	#parse the line
	values = line.split()

	##interesting lines are with vaalues list > 5
	if len(values)>Imagefilepath_index:
		#extract the pathname
		mrcs_path = values[Imagefilepath_index]
		#remove the 6 digit number and the @ sign (what is the 6 digit number for?)
		at_index = mrcs_path.find("@")
		class_number = mrcs_path[:at_index]
		mrcs_path = mrcs_path[at_index+1:]
		#build the full mrcs filepath name by searching for its place
		files = glob.glob(starfile_startsearch+"/**/"+mrcs_path, recursive=True)
		#do the next step:
		# verify the existence (os.path.isfile(path)
		# copy to the right place

		print (class_number, mrcs_path, files)

	print (len(values))

def readstarfile(file):
	with open(file) as f:
		for line in f:
			#print (line)
			extract_mrcsfile(line)
	f.close()

def main():
	for filepath in glob.glob(starfile_startsearch + "/**/particles.star", recursive=True):
		print (filepath)
		readstarfile(filepath)

if __name__ == "__main__":
	main()

