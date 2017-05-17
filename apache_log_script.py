""" program that takes a filename as its only
argument, and outputs the following data:

   Parsed XXX line
   Duration of log file:

   Most requested page:
   Most frequent visitor:

   Min page load time:
   Average page load time:
   Max page load time:

   Number of errors:
   Total data transferred:
"""
import os
import re
from sys import argv, exit
from collections import Counter

#change this variable to point to the location of the apache access log file
#uncomment if you prefer to specify location of file directly
#FILE_LOCATION i= '/var/log/httpd'

if len(argv) !=2:
                print("script needs filename argument")
                exit()

FILE_PATH = os.getcwd()
FILE_NAME = argv[1]
REG_STR = '(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}) +([\w.-]) +([\w.-]) +\[(.*?)\] +"(.*?)" +(\d{3}) +(\d{4}) +"(.*?)" +"(.*?)" +(\d{4})'
REG_KEY = {"visitor":1,"webpage":8,"code":6,"data_size":7,"load_time":10}


def is_valid_file(file_path,file_name):
	if os.path.isfile(file_path+'/'+file_name):
		try:
			with open(file_path+'/'+file_name,'r') as logFile:
				return logFile.readlines()
		except IOError as e:
			exit("error opening file")
	else:
		exit("Log file not found at %s" % file_path)

#collecting the raw logs from log file...
RAW_LOGS = is_valid_file(FILE_PATH,FILE_NAME)

#defining function to process logs using reg expression defined in REG_KEY
def return_reg_groups(param_raw_logs,regkey):
	reg_group = []		#initialize group collector list 
	for objk in param_raw_logs:
		Result = re.search(REG_STR, objk)
		if Result is not None:
			reg_group.append(Result.group(regkey))	#populate list using key param collected from REG_KEY dictionary
		else:
			pass
	return reg_group

def return_page_load_times(param_time,regkey):
	max_page_load_time = max(return_reg_groups(param_time,REG_KEY[regkey]))
	min_page_load_time = min(return_reg_groups(param_time,REG_KEY[regkey]))
	ave_page_load_time = sum(int(load_time) for load_time in return_reg_groups(param_time,REG_KEY[regkey]))/float(len(return_reg_groups(param_time,REG_KEY[regkey])))
	return [max_page_load_time, min_page_load_time, ave_page_load_time]

def return_freq_count(param_freq,regkey):
	return Counter(return_reg_groups(param_freq,REG_KEY[regkey])).most_common()[0][0]

	
def return_data_count(param_data,regkey):
	#re.findall(r'[3-5]\d{2}',l)
	re_count = 0
	for objk in return_reg_groups(param_data,REG_KEY[regkey]):
		Result = re.match(r'[3-5]\d{2}',objk)
		if Result is not None:
			re_count+=1
		else:
			pass

	return [re_count,sum(int(page_size) for page_size in return_reg_groups(param_data,REG_KEY[regkey]))]


print('Most frequent visitor: %s' % (return_freq_count(RAW_LOGS,"visitor")))
print('Most visited page: %s' % (return_freq_count(RAW_LOGS,"webpage")))
print('Number of errors: %s' % (return_data_count(RAW_LOGS,"code")[0]))
print('Total number of data transfered: %s' % (return_data_count(RAW_LOGS,"data_size")[1]))
print('Max page load time: %s' % (return_page_load_times(RAW_LOGS,"load_time")[0]))
print('Minimum page load time: %s' % (return_page_load_times(RAW_LOGS,"load_time")[1]))
print('Average page load time: %6.2f' % (return_page_load_times(RAW_LOGS,"load_time")[2]))
#print(return_reg_groups(RAW_LOGS,"load_time"))
