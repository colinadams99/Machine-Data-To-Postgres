


# initializing IP address
ip = "555.555.55.55"

machine = "Machine1Data"
#machine = "Machine1"

# setup connection
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="your_password_here"
)

while machine == "Machine1Data":
    response = requests.get('http://' + ip + "/api/deviceData/" + machine)
    data = json.loads(response.text)
     
    haas_time = datetime.datetime.fromtimestamp(data['coolant_level']['timestamp'],
                                                pytz.timezone('US/Eastern'))
    coolant_level = data['coolant_level']['value']
    spindle_rpm = data['spindle_rpm']['value']
    mach_x = data['machine_x']['value']
    
    cur = conn.cursor()
    cur.execute("INSERT INTO lf.haas (machine1_time, coolant_level, spindle_rpm, mach_x) VALUES (%s, %s, %s, %s)", (machine1_time, coolant_level, spindle_rpm, mach_x,))
    # Commit the change
    conn.commit()   
    
    print(machine1_time)
    
    time.sleep(1)
    

while machine == "Machine2":
    response = requests.get('http://' + ip + "/api/deviceData/" + machine)
    data = json.loads(response.text)
   
    time_logged = datetime.datetime.fromtimestamp(int(datetime.datetime.now().timestamp()),pytz.timezone('US/Eastern'))
    
    time_plus = time_logged + datetime.timedelta(minutes = 3)
    #time_plus = datetime.datetime.fromtimestamp(time_plus, pytz.timezone('US/Eastern'))
    time_minus = time_logged - datetime.timedelta(minutes = 3)
    #time_minus = datetime.datetime.fromtimestamp(time_minus, pytz.timezone('US/Eastern'))
   
    mach2_x_val = data['x']['value']
    mach2_x_time = datetime.datetime.fromtimestamp(data['x']['timestamp'], 
                                                 pytz.timezone('US/Eastern'))
    mach2_y_val = data['y']['value']
    mach2_y_time = datetime.datetime.fromtimestamp(data['y']['timestamp'],
                                                 pytz.timezone('US/Eastern'))
    mach2_y_val = data['y']['value']
    mach2_z_time = datetime.datetime.fromtimestamp(data['z']['timestamp'],
                                                 pytz.timezone('US/Eastern'))
    mach2_rx_val = data['rx']['value']
    mach2_rx_time = datetime.datetime.fromtimestamp(data['rx']['timestamp'],
                                                 pytz.timezone('US/Eastern'))
    mach2_ry_val = data['ry']['value']
    mach2_ry_time = datetime.datetime.fromtimestamp(data['ry']['timestamp'],
                                                 pytz.timezone('US/Eastern'))
    mach2_rz_val = data['rz']['value']
    mach2_rz_time = datetime.datetime.fromtimestamp(data['rz']['timestamp'],
                                                 pytz.timezone('US/Eastern'))

    mach2_times = [mach2_x_time, mach2_y_time, mach2_z_time, mach2_rx_time, mach2_ry_time, mach2_rz_time]
    
    print(mach2_x_time)
    print(time_logged)
    #print(time_buf)
    print("")   
    
    for i_time in mach2_times:
        if i_time < time_plus and i_time > time_minus:
            
            cur = conn.cursor()
            cur.execute("INSERT INTO lf.mach2 (x_val, x_time, y_val, y_time, z_val, z_time, rx_val, rx_time, ry_val, ry_time, rz_val, rz_time, time_logged) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (mach2_x_val, mach2_x_time, mach2_y_val, mach2_y_time, mach2_z_val, mach2_z_time, mach2_rx_val, mach2_rx_time, mach2_ry_val, mach2_ry_time, mach2_rz_val, mach2_rz_time, time_logged,))
            # Commit the changes
            conn.commit()   
        
    time.sleep(5)
