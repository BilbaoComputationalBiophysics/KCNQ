import pandas as pd
import numpy as np
from collections import defaultdict
import math

	#############################################################
	# DESCRIPTION: script for parsing document: brain_data.xlsx #
	#############################################################
#Usage: python read_excel.py making sure that the following path is correct

# 1. The script initializes two dictionaries, brain_left y brain_right, which will be used to 
# store the data from experiments, the entries will be "mice_region": 0.5h_Outside ...
# 2. Reads the data and stores the different experimental outcomes into the previous 
# dictionaries, in this step we delete percentage vales above 100%
# 3. Makes the mean values over experiments and merges the data between right and left 
# dictionaries, no extra conditions are required for the values to be merged (it could be
# that if left value is 10 times the right one, both are catalogued as nonsense) 
 
Excel_file = pd.ExcelFile('/home/oscar/oscar/brain_project/brain_data.xlsx')  #read excel with pandas:
#print(Excel_file.sheet_names) # see all sheet names

# 1. Loop for initialize the dictionaries: 
brain_left = defaultdict(dict)
brain_right = defaultdict(dict)
brain= defaultdict(dict)
for sheets in Excel_file.sheet_names: #inicialize left and right dictionaries,
	df = pd.read_excel(Excel_file, sheet_name=sheets)
	for index, row in df.iterrows(): #iterate over excel sheets:
		if (row[2]=='left') and not (pd.isna(row[1])):
			dict_key=str(row[0])+'_'+str(row[1]) #Keys are named like this: "naive_Outside"
			brain_left[dict_key]=[]
		if (row[2]=='right') and not (pd.isna(row[1])):
			dict_key=str(row[0])+'_'+str(row[1]) 
			brain_right[dict_key]=[]	
			
# 2. Reading loop, populate the dictionaries:
for sheets in Excel_file.sheet_names:
	df = pd.read_excel(Excel_file, sheet_name=sheets)
	# print example sheet (outside, the first one)
	if sheets=="Outside":
		print(df)
	#iterate over rows of the sheet:	
	for index,row in df.iterrows():
		if (row[2]=='left') and not (pd.isna(row[1])): # selecting left and not NAN values
			if float(row[6]) <= 100: # check that percentages make sense
				dict_key=str(row[0])+'_'+str(row[1]) 	
				brain_left[dict_key].append(float(row[6]))  # ---> {naive_Outside: [value1, value2..] 0.5h_Outside: [value1..], ....}+++
		if (row[2]=='right') and not (pd.isna(row[1])):  # same for the right brain
			if float(row[6]) <= 100: # check that percentages make sense	
				dict_key=str(row[0])+'_'+str(row[1]) 	
				brain_right[dict_key].append(float(row[6]))



# 3. Make the mean values of both dictionaries and merge into brain directory:
for key in  list(set(brain_left.keys()) | set(brain_right.keys())): #iterating over all keys appearing in both dictionaries
	if (len(brain_left[str(key)])>0) and (len(brain_right[str(key)])>0): # we have info for left and right
		mean_left = sum(np.array(brain_left[str(key)]))/len(brain_left[str(key)])
		mean_right = sum(np.array(brain_right[str(key)]))/len(brain_right[str(key)])
		brain[str(key)]=0.5*(mean_left+mean_right)
	if (len(brain_left[str(key)])==0) and (len(brain_right[str(key)])>0): # we have info only for right
		brain[str(key)]=sum(np.array(brain_right[str(key)]))/len(brain_right[str(key)])
	if (len(brain_left[str(key)])>0) and (len(brain_right[str(key)])==0): # we have info only for left
		brain[str(key)]=sum(np.array(brain_left[str(key)]))/len(brain_left[str(key)])	
