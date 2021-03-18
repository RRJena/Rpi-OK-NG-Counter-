#DB API LIBRARY
import sqlite3
from sqlite3 import Error
global model
global OK
global NGd
global device_time_stamp
global device_date
global device_time
global database
global duration_in_s
database="autoprn.db"
duration_in_s=10
OK=100
NG=10
model="SHAFT FOR YRA TOWER"
device_time_stamp="2021-03-10 07:00:00"
device_time="07:00:00"
device_date='2021-03-10'
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn
def update_data_db():
    global model
    global OK
    global NG
    global device_time_stamp
    global device_date
    global device_time
    global database
    last_data_db_ok=0
    last_data_db_ng=0
    last_data_db_date=""
    OK=1
    if not (model == None or model == ''):
        try:
            conn = create_connection(database)
            command="SELECT * FROM data WHERE model='"+str(model)+"' AND date='"+str(device_date)+"'"
            print(command)
            cursor = conn.execute(command)
            data=cursor.fetchall()
            if len(data)>0:
                for row in data:
                    #last_data_db_date=str(row[1])
                    print("hello")
                    last_data_db_ok=int(row[4])
                    last_data_db_ng=int(row[5])
                print(last_data_db_ok,last_data_db_ng)
            else:
                print("Data")
            conn.close()
        except sqlite3.Error as er:
            print("errior"+str(er))
        
                
update_data_db()