import subprocess
from sys import stdout
from datetime import datetime
<<<<<<< HEAD
import paramiko, csv, os, re, time, socket, math


# Update the next three lines with your
# server's information

host = "192.168.50.1"
username = "admin"
password = "StageCFNS2022!"
port = "8822"
MNO = ""
com = "get system"


def getData(com):

    output=""
=======
import paramiko
import csv
import socket
import re
import requests

# Update these with your server's information
host = "192.168.10.1"
username = "admin"
password = "StageCFNS2022!"
port = 8822
api_key = "pk.f6e2aa2d0a8c4e9f9a2ffc1fe6904c74"  # Replace with your actual API key

def get_data(command):
    output = ""
>>>>>>> 0c5826d (bewerkte meetkast script, nu met; GPS coordinaten, cell tower informatie.)
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password, port=port)

<<<<<<< HEAD

    stdin, stdout, stderr = client.exec_command(com)
    print ("ssh succuessful. Closing connection")
    stdout=stdout.readlines()
    client.close()

    for line in stdout:
        output=output+line
    #als er geen verbinding is houdt het leeg
    if "Connected" not in output:
        print ("Not connected")
        Signalstrength = ",,,"
        return Signalstrength
        
    else:
        print (output)
        
    SINR = re.search('SINR                       : (.*)dB', output)
    RSRP = re.search('RSRP                       : (.*)dB', output)
    RSRQ = re.search('RSRQ                       : (.*)dB', output)
    conn = re.search('Network                    : (.*)\n', output)
    
    SINRres = SINR.group(1)
    RSRPres = RSRP.group(1)
    RSRQres = RSRQ.group(1)
    connres = conn.group(1)
    Signalstrength =  RSRQres + "," + RSRPres + "," + SINRres + ","  + connres
    
    return Signalstrength

def getGPS():
    thePort = 60660
    #Function decimalToDM (Decimal to Degrees & Mins)
    #Convert the decimal-decimal degree value in the NEMA message to degrees and minutes
    #eg 5141.058053 (ddmm.mmmmmm) = 51 41.058053 = 51 + 41.058053/60 = 51.684301 degrees
    def decimalToDM( nemaIn ):
        #move decimal point for manipulation
        theDegrees= nemaIn / 100
        
        #create tuple of degrees and mins
        degsAndMins = math.modf(theDegrees)
        
        #Grab the Degrees as an integer
        theDegrees = int(degsAndMins[1]) 
        
        #restore original decimal point location
        theMins = degsAndMins[0] *100
        
        #grab the mins
        theMins=round(theMins,6)
        
        #convert decimal minutes to mins
        convertedMins=theMins/60
        
        #Add the degrees and mins together
        convertedResult=str(round(theDegrees + convertedMins,6))
        
        return convertedResult; 

    #Set up a client socket to connect to the GPS enabled device
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(5)
    #Connect to the device on the right Ip & port
    try:
        client_socket.connect((host, thePort))
    except socket.timeout:
        print("Can't connect to "+host+" on port "+str(thePort)+" : Timeout")
        quit()

    #Whilst we've received a response from the socket...
    data = client_socket.recv(1024)
    gps = "0,0"
    # make sure we actually have some data (and not just a response).
    if len(data) > 0:
        #decode the data from byte to string to make working with it easier
        print (data)
        thedata=data.decode('ascii')
        # split the data into a list of lines
        lines = thedata.splitlines(1)
        # iterate over each line
        for line in lines:
            #Data sent is coimma delimited so lets split it
            gpsstring = line.split(',')
            #if the first column contains $GPRMC and
            #if it has enough elements we have hit paydirt
            if gpsstring[0] == '$GPRMC' and len(gpsstring)>6:
                #check that there is returned GPS data
                if gpsstring[3]:
                    #Get Lat and Long String by converting decimals and adding compass pos
                    theLat = decimalToDM(float(gpsstring[3])) + (gpsstring[4])
                    theLong = decimalToDM(float(gpsstring[5])) + (gpsstring[6])
                    print ("Lat: " + theLat)
                    print ("Long: " + theLong)
                    
                    gps = theLat +","+ theLong
                    #Wait 5 secs 
                    time.sleep(5)           		
    return gps

def WriteToCSV():
    with open('modem.csv', 'w', newline='') as output_fn:
        timeStamp = datetime.now().strftime('%d-%m-%Y %H:%M')
        wr = csv.writer(output_fn, quoting=csv.QUOTE_NONE, escapechar=' ', delimiter= ',')
        print("writing to csv...")
        wr.writerow(["mno, RSRQ, RSRP, SINR, type, tijd, lat, long"]) 
        wr.writerow(["Vodafone", getData("get wan 4"), timeStamp, getGPS()])   
        wr.writerow(["T-Mobile", getData("get wan 5"), timeStamp, getGPS()]) 
        wr.writerow(["KPN", getData("get wan 6"), timeStamp, getGPS()]) 
        wr.writerow(["Tampnet", getData("get wan 7"), timeStamp, getGPS()]) 
    #print(getData("get wan 4"))
    subprocess.run(["psql",  "-f", "/home/cfns/systemtest/copymodem.sql", "postgres://postgres:stagecfns@localhost:5432/postgres"])
    
WriteToCSV()
=======
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode()
    client.close()

    if "Connected" not in output:
        print("Not connected")
        return "0.0,0.0,0.0,N/A"  # Use default values

    SINR = re.search(r'SINR\s+:\s+(.*)dB', output)
    RSRP = re.search(r'RSRP\s+:\s+(.*)dB', output)
    RSRQ = re.search(r'RSRQ\s+:\s+(.*)dB', output)
    conn = re.search(r'Network\s+:\s+(.*)', output)

    SINR_res = float(SINR.group(1)) if SINR else 0.0
    RSRP_res = float(RSRP.group(1)) if RSRP else 0.0
    RSRQ_res = float(RSRQ.group(1)) if RSRQ else 0.0
    conn_res = conn.group(1) if conn else "N/A"

    return f"{RSRQ_res},{RSRP_res},{SINR_res},{conn_res}"

def decimal_to_dm(nema_in):
    the_degrees = int(nema_in / 100)
    the_minutes = nema_in - (the_degrees * 100)
    return round(the_degrees + (the_minutes / 60), 6)

def get_gps():
    the_port = 60660
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(5)

    try:
        client_socket.connect((host, the_port))
    except socket.timeout:
        print(f"Can't connect to {host} on port {the_port}: Timeout")
        return "0.0,0.0"  # Default values

    data = client_socket.recv(1024)
    gps = "0.0,0.0"
    if len(data) > 0:
        the_data = data.decode('ascii')
        lines = the_data.splitlines()

        for line in lines:
            gps_string = line.split(',')
            if gps_string[0] == '$GPRMC' and len(gps_string) > 6:
                lat_decimal = decimal_to_dm(float(gps_string[3]))
                if gps_string[4] == 'S':
                    lat_decimal = -lat_decimal  # Make negative if South

                long_decimal = decimal_to_dm(float(gps_string[5]))
                if gps_string[6] == 'W':
                    long_decimal = -long_decimal  # Make negative if West

                gps = f"{lat_decimal},{long_decimal}"
                break  # Exit loop after finding valid GPS data

    return gps

def get_cell_tower_info(conn_id):
    session = requests.Session()
    login_url = f"http://{host}/api/login"
    login_data = {'username': username, 'password': password}
    response = session.post(login_url, json=login_data, verify=False)

    if response.status_code == 200 and response.json().get("stat") == "ok":
        url = f"http://{host}/api/status.wan.connection"
        params = {'id': conn_id}
        response = session.get(url, params=params, verify=False)

        if response.status_code == 200:
            data = response.json()
            if 'response' in data and str(conn_id) in data['response']:
                wan_info = data['response'][str(conn_id)]
                if 'cellular' in wan_info and 'cellTower' in wan_info['cellular']:
                    cell_tower = wan_info['cellular']['cellTower']
                    cell_id = cell_tower.get('cellId')
                    cell_plmn = cell_tower.get('cellPlmn')
                    cell_utran_id = cell_tower.get('cellUtranId')
                    tac_lac = cell_tower.get('tac')

                    return cell_plmn, tac_lac, cell_utran_id

    return None, None, None, None  # Default values if not found

def write_to_csv():
    with open('modem.csv', 'w', newline='') as output_fn:
        time_stamp = datetime.now().strftime('%d-%m-%Y %H:%M')
        wr = csv.writer(output_fn, quoting=csv.QUOTE_MINIMAL, delimiter=',')
        print("Writing to CSV...")
        wr.writerow(["mno", "rsrq", "rsrp", "sinr", "type", "tijd", "lat", "long", "cell_plmn", "tac_lac", "cell_utran_id"])

        for mno, command in [("Vodafone", "get wan 4"), 
                             ("T-Mobile", "get wan 5"), 
                             ("KPN", "get wan 6"), 
                             ("Tampnet", "get wan 7")]:
            data = get_data(command).split(",")
            gps = get_gps().split(",")
            conn_id = command.split()[-1]  # Example: extract ID from command
            cell_info = get_cell_tower_info(conn_id)

            # Ensure data has the correct number of elements
            while len(data) < 3:
                data.append("0.0")  # Default values for RSRQ, RSRP, SINR
            
            connection_type = data[3] if len(data) > 3 else "N/A"

            # Replace None or empty values in cell info with default values
            cell_plmn = cell_info[0] if cell_info[0] is not None else 0
            tac_lac = cell_info[1] if cell_info[1] is not None else 0
            cell_utran_id = cell_info[2] if cell_info[2] is not None else 0

            # Write the row
            wr.writerow([mno] + data[:3] + [connection_type] + [time_stamp] + gps + [cell_plmn, tac_lac, cell_utran_id])

    # Execute SQL script
    subprocess.run(["psql", "-f", "/home/cfns/systemtest/copymodem.sql", "postgres://postgres:stagecfns@localhost:5432/postgres"])

if __name__ == "__main__":
    write_to_csv()
>>>>>>> 0c5826d (bewerkte meetkast script, nu met; GPS coordinaten, cell tower informatie.)
