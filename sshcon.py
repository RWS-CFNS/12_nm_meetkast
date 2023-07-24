import subprocess
from sys import stdout
from datetime import datetime
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
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password, port=port)


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
