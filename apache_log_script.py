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
from datetime import datetime

#change this variable to point to the location of the apache access log file
#uncomment if you prefer to specify location of file directly
#FILE_LOCATION i= '/var/log/httpd'

if len(argv) !=2:
                print("script needs filename argument")
                exit()

FILE_PATH = os.getcwd()
FILE_NAME = argv[1]
REG_STR = '(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}) +([\w.-]) +([\w.-]) +\[(.*?)\] +"(.*?)" +(\d{3}) +(\d{4}) +"(.*?)" +"(.*?)" +(\d{4})'
REG_KEY = {"visitor":1,"log_time":4,"webpage":8,"code":6,"data_size":7,"load_time":10}


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

def return_total_log_time(param_raw_logs,regkey):
	time_obj = []
	for objk in return_reg_groups(param_raw_logs,REG_KEY[regkey]):
		objj = objk.split(" ")
		time_obj.append(objj[0])
	
	log_start_time = datetime.strptime(time_obj[0], "%d/%b/%Y:%H:%M:%S")
	log_end_time = datetime.strptime(time_obj[-1], "%d/%b/%Y:%H:%M:%S")
	return (log_end_time - log_start_time).total_seconds()
	

def return_page_load_times(param_raw_logs,regkey):
	max_page_load_time = max(return_reg_groups(param_raw_logs,REG_KEY[regkey]))
	min_page_load_time = min(return_reg_groups(param_raw_logs,REG_KEY[regkey]))
	ave_page_load_time = sum(int(load_time) for load_time in return_reg_groups(param_raw_logs,REG_KEY[regkey]))/float(len(return_reg_groups(param_raw_logs,REG_KEY[regkey])))
	return [max_page_load_time, min_page_load_time, ave_page_load_time]

def return_freq_count(param_raw_logs,regkey):
	return Counter(return_reg_groups(param_raw_logs,REG_KEY[regkey])).most_common()[0][0]

	
def return_data_count(param_raw_logs,regkey):
	#re.findall(r'[3-5]\d{2}',l)
	re_count = 0
	for objk in return_reg_groups(param_raw_logs,REG_KEY[regkey]):
		Result = re.match(r'[3-5]\d{2}',objk)
		if Result is not None:
			re_count+=1
		else:
			pass

	return [re_count,sum(int(page_size) for page_size in return_reg_groups(param_raw_logs,REG_KEY[regkey]))]

print('Duration of log file: %6.2f \n' % (return_total_log_time(RAW_LOGS,"log_time")))
print('Most frequent visitor: %s' % (return_freq_count(RAW_LOGS,"visitor")))
print('Most visited page: %s \n' % (return_freq_count(RAW_LOGS,"webpage")))
print('Max page load time: %s' % (return_page_load_times(RAW_LOGS,"load_time")[0]))
print('Minimum page load time: %s' % (return_page_load_times(RAW_LOGS,"load_time")[1]))
print('Average page load time: %6.2f \n' % (return_page_load_times(RAW_LOGS,"load_time")[2]))
print('Number of errors: %s' % (return_data_count(RAW_LOGS,"code")[0]))
print(return_total_log_time(RAW_LOGS,"log_time"))
print('Total data transfered: %s' % (return_data_count(RAW_LOGS,"data_size")[1]))
