import sqlite3
from sqlite3 import Error
import urllib3
import datetime
from datetime import datetime
import time
import pytz
from datetime import timedelta
import log
http = urllib3.PoolManager()
app_path="/home/pi/autoprn/"
url_path='http://192.168.3.19/eol/module/autoprn/API/'
database = app_path+"autoprn.db"
device_id=""
try:
    conn = sqlite3.connect(database)
    command="SELECT device_id from device_details"
    cursor = conn.execute(command)
    data=cursor.fetchall()
        if len(data)>0:
            for row in data:
                device_id=row[2]
    log.writeLog("Deivce ID:",str(device_id))
except sqlite3.Error as er:
    print("SQL ERROR"+str(er))
    log.writeError("SQL Error",str(er))
finally:
    print("Device ID Collected")
    conn.close()


    
#Definition Program to check Online Stat
def check_online_stat():
    import requests
    try:
        if requests.get('http://192.168.3.19',timeout=1).ok:
            #print("You're Online")
            log.writLog("NETWORK STATUS CHECK",str("ONLINE"))
            return True
    except:
        #print("You're Offline")
        log.writeError("Nework Error",str("OFFLINE -or- DISCONNECTED"))
        return False
# SERVR SYNC OPERATION
def sync_data():
    global database
    global device_id
    log.writeLog("Sync Process Data:","Process Statrted")
    if device_id!=None or device_id!="":
            if check_online_stat():
                print("online")
                try:
                    conn = sqlite3.connect(database)
                    command="SELECT * from data WHERE sync=0 LIMIT 10"
                    #print(command)
                    cursor = conn.execute(command)
                    data=cursor.fetchall()
                if len(data)>0:
                    for row in data:
                        OK=
                        NG=
                        model=
                        date=
                else:
                    print("Part Not found with name: "+part)
                    command="INSERT INTO model(part_name) VALUES ('"+str(part)+"')"
                    #print(command)
                    conn.execute(command)
                    conn.commit()
            except sqlite3.Error as er:
                print("SQL ERROR"+str(er))
                log.writeError("INSETRT PART NAME SQL Error:",str(er))
            finally:
                print("Model Updated")
                conn.close()
              
sync_data()
def sync_historian(conn):
    sql=""
    data=""
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    
def sync_signal(conn):
    sql=""
    data=""
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    
def update_model_from_server():
    global database
    process_name=""
    global device_id
    global url_path
    if device_id!=None or device_id!="":
        try:
            conn = sqlite3.connect(database)
            command="SELECT product_name from device_details"
            cursor = conn.execute(command)
            data=cursor.fetchall()
                if len(data)>0:
                    for row in data:
                        process_name=row[5]
         except sqlite3.Error as er:
            print("SQL ERROR"+str(er))
            log.writeError("SQL Error",str(er))
         finally:
            print("Process Name ")
            conn.close()
    
        payload = {'process_name': process_name}
        url = url_path+'getModel.php'
        try:
            req = http.request('GET', url, fields=payload)
        except ConnectionError:
            raise Exception('Unable to get updates after {} seconds of ConnectionErrors'.format(connection_timeout))
            log.writeError("Netrwork Request Error","Unable to get the API requested")
        model=req.data.decode('utf-8')
        model=model.rstrip()
        model=model.lstrip()
        model=model.split(',')
        #model=''.join(model).split()
        #print(model[0])
        for part in model:
            log.writeLog("Part Name Collected:",part)
           if part!='':
                try:
                    conn = sqlite3.connect('autoprn.db')
                    command="SELECT part_name from model WHERE part_name='"+str(part)+"'"
                    #print(command)
                    cursor = conn.execute(command)
                    if cursor.fetchone():
                        log.writeLog("Part Found and Exist ","Part names are found")
                        print("Already Exist!")
                    else:
                        log.writeLog("Part Not Found","No parts are found in DB NEW part Updated")
                        print("Part Not found with name: "+part)
                        command="INSERT INTO model(part_name) VALUES ('"+str(part)+"')"
                        #print(command)
                        conn.execute(command)
                        conn.commit()
                except sqlite3.Error as er:
                    print("SQL ERROR"+str(er))
                    log.writeError("SQL ERROR",str(er))
                finally:
                    print("Model Updated")
                    conn.close()
#update_model_from_server()