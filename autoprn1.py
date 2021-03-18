"""
Project_name: AUTO PRN PROJECT
Author: Rakesh Ranjan Jena
Dept: IMS
Company: BEST KOKI AUTOMOTIVE PVT. LTD.
Start Date:02.03.2021
Implement Date:
End Date:
DESCRIPTION:
This Project is for auto counting of OK NG Parts with Cycle time from each and every Machine.
This is IIoT Prject to Monitor Productivity of Machine and Process through Cycle time and OK,NG Count.
This Project is Applicable where PLC Communcication is Not Possible or PLC is OLDER or PLC is unable to send data to Server.
"""

#IMPORTING LIBRARY
import threading
#GTK Library
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject,GLib
#DATE and TIME Library
import datetime
from datetime import datetime
import time
import pytz
from datetime import timedelta
#DB API LIBRARY
import sqlite3
from sqlite3 import Error
#Rpi GPIO
import RPi.GPIO as GPIO
#URL LIBRARY
import urllib3
http = urllib3.PoolManager()

from gi.repository import Gtk
app_path="/home/pi/autoprn/"
database = app_path+"autoprn.db"
class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()
# GLOBAL VARIABLES
device_id="BK-IMS-2021-DEV100"
device_time_stamp=datetime.now()
#variable Declaration For Timer Operation
start_count_signal=0
#GPIO Operation VARIABLES
OK=0
NG=0
model=""
remark=""
now = datetime.now(tz=pytz.timezone('Asia/Kolkata'))
device_time_stamp=(str(now.strftime('%Y-%m-%d %H:%M:%S-%f')))
device_date=(str(now.strftime('%Y-%m-%d')))
device_time=(str(now.strftime('%H:%M:%S')))
#DB CONNECTION
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

#Update Model DB
def update_model_from_server():
    global database
    payload = {'process_name': 'SHAFT GRINDING'}
    url = 'http://192.168.3.19/eol/module/autoprn/API/getModel.php'
    try:
        req = http.request('GET', url, fields=payload)
    except ConnectionError:
        raise Exception('Unable to get updates after {} seconds of ConnectionErrors'.format(connection_timeout))
    model=req.data.decode('utf-8')
    model=model.rstrip()
    model=model.lstrip()
    model=model.split(',')
    #model=''.join(model).split()
    #print(model[0])
    for part in model:
        if part!='':
            try:
                conn = create_connection(database)
                command="SELECT part_name from model WHERE part_name='"+str(part)+"'"
                #print(command)
                cursor = conn.execute(command)
                if cursor.fetchone():
                    print("Already Exist!")
                else:
                    print("Part Not found with name: "+part)
                    command="INSERT INTO model(part_name) VALUES ('"+str(part)+"')"
                    #print(command)
                    conn.execute(command)
                    conn.commit()
            except sqlite3.Error as er:
                print("SQL ERROR"+str(er))
            finally:
                print("Model Updated")
                conn.close()

#UODATE MODEL CALL
update_model_from_server()
#DB OPEERATIONS
def update_data_db():
    global model
    global OK
    global NG
    global device_time_stamp
    global device_date
    global device_time
    global database
    #last_data_db_ok=0
    #last_data_db_ng=0
    #last_data_db_date=""
    if not (model == None or model == ''):
        try:
            conn = create_connection(database)
            command="SELECT * FROM data WHERE model='"+str(model)+"' AND date='"+str(device_date)+"'"
            #print(command)
            cursor = conn.execute(command)
            data_1=cursor.fetchall()
            if len(data_1)>0:
                for row in data_1:
                    #last_data_db_date=str(row[1])
                    last_data_db_ok=int(row[4])
                    last_data_db_ng=int(row[5])
                print(last_data_db_ok,last_data_db_ng)
    
                if OK<last_data_db_ok or NG<last_data_db_ng:
                    #NEW DATA ADDED
                    OK+=last_data_db_ok
                    NG+=last_data_db_ng
                    
                print("Data Updated")
                command="UPDATE data SET date='"+device_date+"',time='"+device_time+"',OK="+str(OK)+",NG="+str(NG)+",time_stamp='"+str(device_time_stamp)+"',sync=0 WHERE model='"+str(model)+"' AND date='"+str(device_date)+"'"
                #print(command)
                #conn.commit()
            else:
                print("Part Model found with name, New Addition: "+model)
                command="INSERT INTO data(date,time,model,OK,NG,time_stamp,sync) VALUES ('"+device_date+"','"+device_time+"','"+str(model)+"',"+str(OK)+","+str(NG)+",'"+str(device_time_stamp)+"',0)"
                #print(command)
            conn.execute(command)
            conn.commit()
                
        except sqlite3.Error as er:
            print("SQL ERROR"+str(er))
        finally:
            conn.commit()
            print("Data Updated")
            conn.close()
    
def create_historian_data():
    global prev_OK
    global prev_NG
    global model
    global OK
    global NG
    global device_time_stamp
    global device_date
    global device_time
    global database
    global duration_in_s
    global idle_time_in_sec
    global remark
    if not ((OK == prev_OK and NG == prev_NG) or (model == None or model == '')):
        try:
            conn = create_connection(database)
            command="INSERT INTO historian(model,date,time,OK,NG,time_stamp,cycle_time,idle_time,remark) VALUES ('"+str(device_date)+"','"+str(device_time)+"','"+str(model)+"',"+str(OK)+","+str(NG)+",'"+str(device_time_stamp)+"','"+str(duration_in_s)+"',"+str(idle_time_in_sec)+",'"+str(remark)+"')"
            #print(command)
            conn.execute(command)
            conn.commit()
        except sqlite3.Error as er:
            print("SQL ERROR"+str(er))
        finally:
            print("History Updated")
            conn.close()
            prev_OK=OK
            prev_NG=NG
            idle_time_in_sec=0
    else:
        print("Same Data")
    






def main():
    global database
    database = app_path+"autoprn.db"
    conn = create_connection(database)
    builder = Gtk.Builder()
    builder.add_from_file(app_path+"autoprn.glade")
    builder.connect_signals(Handler())
    #GET GUI Objects
    date_label= builder.get_object("date_label")
    shift_label= builder.get_object("shift_label")
    model_box= builder.get_object("model_box")
    count_btn= builder.get_object("count_btn")
    OK_label= builder.get_object("OK_label")
    NG_label= builder.get_object("NG_label")
    #Sensor Labels
    inp1_label= builder.get_object("inp1_label")
    inp2_label= builder.get_object("inp2_label")
    inp3_label= builder.get_object("inp3_label")
    inp4_label= builder.get_object("inp4_label")
    inp5_label= builder.get_object("inp5_label")
    inp6_label= builder.get_object("inp6_label")
    #OUTPUT Label
    out1_label= builder.get_object("out1_label")
    out2_label= builder.get_object("out2_label")
    #Target and Completed Label
    target_label= builder.get_object("target_label")
    completed_label= builder.get_object("completed_label")
    device_id_label= builder.get_object("device_id_label")
    info_label= builder.get_object("info_label")
    cycle_time_label= builder.get_object("cycle_time_label")
    idle_time_label= builder.get_object("idle_time_label")
    btn_man=builder.get_object("btn_man")
    btn_machine=builder.get_object("btn_machine")
    btn_material=builder.get_object("btn_material")
    btn_method=builder.get_object("btn_method")
    def update_model_data():
        try:
            conn = sqlite3.connect(database)
            command="SELECT part_name from model"
            #print(command)
            cursor = conn.execute(command)
            for row in cursor:
                model_box.append_text(row[0])
        except sqlite3.Error as er:
                print("SQL ERROR"+str(er))
        finally:
                print("Model Updated")
                conn.close()
    update_model_data()
    def get_device_id():
        sql=""
        data=""
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()
    def update_local_time():
        global device_time_stamp
        global device_date
        global device_time
        now = datetime.now(tz=pytz.timezone('Asia/Kolkata'))
        date_label.set_text(str(now.strftime('%B %d, %Y %H:%M:%S')))
        device_time_stamp=(str(now.strftime('%Y-%m-%d %H:%M:%S-%f')))
        device_date=(str(now.strftime('%Y-%m-%d')))
        device_time=(str(now.strftime('%H:%M:%S')))

        #print(device_time_stamp)
    def update_data_model(self):
            global model
            global OK
            global NG
            OK=0
            NG=0
            model=model_box.get_active_text()
            #if start_count_signal==1:
            info_label.set_text("Selected Part: " + str(model))
            if model==None:
                start_count_signal=0
            else:
                start_count_signal=1
            print(start_count_signal)
          
    count_btn.connect("clicked",update_data_model)
    #Definition to Set OK and NG =o if Model is undeified. Print UIUX and Database
    def update_data():
        global OK
        global NG
        global model
        global in1
        global in3
        if model==None or model=="":
            OK=0
            NG=0
        OK_label.set_text(str(OK))
        NG_label.set_text(str(NG))
        inp1_label.set_text(str(in1))
        inp2_label.set_text(str(in3))
        
        #print("Hello WORLD  1")
    def update_cycle_time():
        global dle_time_in_sec
        global duration_in_s
        idle_time_label.set_text(str(idle_time_in_sec))
        cycle_time_label.set_text(str(duration_in_s))

    
    def main_target():
        global prev_OK
        global prev_NG
        global OK
        global NG
        global idle_time_in_sec
        global duration_in_s
        global in1
        global in3
        prev_OK=0
        prev_NG=0
        idle_time_in_sec=0
        duration_in_s=0
        input_pin1=16
        input_pin2=12
        input_pin3=26
        output_pin1=20
        output_pin2=21
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(input_pin1, GPIO.IN)
        GPIO.setup(input_pin2, GPIO.IN)
        GPIO.setup(input_pin3, GPIO.IN)
        GPIO.setup(output_pin1, GPIO.OUT)
        GPIO.setup(output_pin2, GPIO.OUT)
        
        while True:
            duration_in_sec=0
            idle_count_flag=0
            idle_time_start=datetime.now()
            #sensor and Pin Configuration Variables, I/O Pin Varibles
            d1=0
            d0=0
            in1=GPIO.input(input_pin1)
            in2=GPIO.input(input_pin2)
            in3=GPIO.input(input_pin3)
            #Momnitor Sensor Value Loop
            while in1==0:
                #start Cycle  Time Count
                if idle_count_flag==0:
                    idle_count_flag=1
                    first_time = datetime.now()
                print("OK Loop")
                in1=GPIO.input(input_pin1)
                in3=GPIO.input(input_pin3)
                if in1==1:
                    OK+=1
                if in3==0:
                    d0+=1
                if in3==1:
                    if d0>=1:
                        NG+=1
                        d0=0
                print("d0:"+str(d0))
                print(OK, NG)
            while in3==0:
                if idle_count_flag==0:
                    idle_count_flag=1
                    first_time = datetime.now()
                print("In NG Loop")
                in3=GPIO.input(input_pin3)
                in1=GPIO.input(input_pin1)
                if in3==1:
                    NG+=1
                if in1==0:
                    d1+=1
                if in1==1:
                    if d1>=1:
                        OK+=1
                        d1=0
                print("d1:"+str(d1))
                print(OK, NG)             
            print(model,OK, NG)
            #if model !=None and model==!="" 
            print(in1,in3)
            print(prev_OK,prev_NG)
            #time.sleep(1)
            
            #GLib.idle_add()
            
            
            later_time = datetime.now()
            if idle_count_flag==0:
                difference=0
                duration_in_sec=0
                difference = later_time-idle_time_start
                duration_in_sec = float(difference.total_seconds())*10
                idle_time_in_sec += round(duration_in_sec,4)
                #idle_time_in_sec=idle_time_in_sec
                print("Idle Time"+str(idle_time_in_sec))
            else:
                difference = later_time - first_time
                duration_in_s = float(difference.total_seconds())
                print("Cycle Time"+ str(duration_in_s))
                create_historian_data()
                update_data_db()
                #idle_time_in_sec=0
                
            GLib.idle_add(update_cycle_time)
            GLib.idle_add(update_data)
            GLib.idle_add(update_local_time)
            #GLib.idle_add(update_data_db)
            
            #difference = later_time - first_time
            
            time.sleep(0.01)
        GPIO.cleanup()

    thread = threading.Thread(target=main_target)
    thread.daemon = True
    thread.start() 
    #update Date and Time

    window = builder.get_object("window1")
    window.fullscreen()
    window.show_all()
    
    window.connect("destroy", Gtk.main_quit)
    #GObject.timeout_add(100, print("Hello"))
    Gtk.main()
        
if __name__ == '__main__':
    main()
    

