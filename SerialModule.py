'''
Author: Ashish Kumar
Date: December 09, 2023

Serial Receive Python: Module for serial communication
This allows us to write/send commands to serial.
Now the focus has been on sending, in later revisions reception will be added.
'''

import serial
import time

# function to initialize 
def initConnection(portNo, baudRate):
    '''
    Function to initialize serial connection. 
    Args:
        portNo: (string) The serial port you want to connect to.
        baudRate: (int) The signals per second, i.e., signal transmission speed
    Returns:
        Serial object
    '''
    try:                                           
        # try block because sometimes it fails
        ser = serial.Serial(portNo, baudRate)
        print("Device Connected Successfully!")
        return ser
    except:
        print("Not Connected!")


# function to send data to the serial port
def sendData(se, data, digits):
    '''
    This function formats the data, where each value will have 
    the digits specified. Then sends the data to the serial object.
    Args:
        se: Serial object
        data (list of ints): data to send in list format
        digits (int): digits per value
    Example:
        sendData(ser, [20,30], 3) sends the string "$020030"
    '''
    myString = '$'
    for d in data:
        myString += str(d).zfill(digits)

    try:
        se.write(myString.encode())
        print(myString)
    except:
        print("Data Transmission Failed!")


if __name__ == "__main__":
    port = '/dev/ttyACM0'                     # Arduino UNO
    # port = '/dev/ttyUSB0'                     # SmartElex Board
    ser = initConnection(port, 9600)
    while True:
        sendData(ser, [50,255], 3)
        sendData(ser, [0, 0], 3)

        