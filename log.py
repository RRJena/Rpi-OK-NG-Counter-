from datetime import datetime
import time
import pytz
from datetime import timedelta
app_path="/home/pi/autoprn/log/"
now = datetime.now(tz=pytz.timezone('Asia/Kolkata'))
device_time_stamp=(str(now.strftime('%Y-%m-%d %H:%M:%S-%f')))
device_date=(str(now.strftime('%Y-%m-%d')))
device_time=(str(now.strftime('%H:%M:%S')))
#log_functions
def writeLog(logName,logData):
    global device_date
    global device_time_stamp
    file_name=app_path+"process/Process Log: "+str(device_date)+".txt"
    file1 = open(file_name, "a+")  # append mode 
    file1.write(str(device_time_stamp)+" : Process Name: "+str(logName)+" \n"+str(logData)+"\n") 
    file1.close()

def writeError(errorName,errorData):
    global device_date
    global device_time_stamp
    file_name=app_path+"error/Error Log: "+str(device_date)+".txt"
    file1 = open(file_name, "a+")  # append mode 
    file1.write(str(device_time_stamp)+" : Error Name: "+str(errorName)+" \n"+str(errorData)+"\n") 
    file1.close()