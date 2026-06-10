"""
Basic program that uses the socket library to scan ports on a specified IP address.
Prompts user for both fields. Has a rudimentary loading screen, also tracks time taken for scan.

Author: T.C. Hopkins
Date: 10/06/2026
"""

import socket
import time
import sys
import threading

#Scans port of a specific IP for a specified length of time
def port_scan(target_ip, port, timeout):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Creates an object which specifies IPv4 and TCP will be used
        s.settimeout(timeout) #Sets the timeout using parameter passed by user
        s.connect((target_ip, port)) #Tries to connect to specified port using target IP
        s.close() #If the connection can be created, it then closes the connection and returns True
        return True
    except socket.error:
        return False #If a connection can't be made, an exception is raised and returns false

#Simple loading animation as the port scan takes time
def loading(): #No parameters required
    while working: #Until working = False continues to loop
        for dots in ['', '.', '..', '...']: #Iterates ellipses to show working
            if not working: #When working becomes False loop breaks
                break
            sys.stdout.write(f'\rScanning{dots}   ') #Writes to the terminal object
            sys.stdout.flush() #Removes previous output
            time.sleep(0.3) #Brief pause before next loop
    sys.stdout.write('\rComplete!        \n') #When loop breaks overwrites any previous output

print("Welcome to the Port Scanner Program")
print("RECONNAISSANCE ON A DEVICE YOU DO NOT OWN IS ILLEGAL!")

instruction = "yes"

while instruction == "yes" or instruction == "y":
    #User input fields
    try:
        user_ipv4 = input("\nPlease enter the desired IPv4 address: ")
        print("\nEnter the desired port range.\nPort range is inclusive.")
        user_port_start = int(input("\nPlease enter the starting port: "))
        user_port_end = int(input("Please enter the final port: "))
        user_timeout = float(input("\nPlease enter the timeout in seconds: "))
    except (ValueError): #Handles incorrect value, loops back to beginning
        print("Invalid input. Please try again.")
        continue
    except KeyboardInterrupt: #Keyboard interrupt breaks loop and ends program gracefully
        print("\nExiting...")
        break

    #Some invalid input handling, makes sure ports are between 1 - 65535
    #Ensures start point is less than end point which would scan zero ports
    #Invalid input just continues loop
    if user_port_start > user_port_end:
        print("\nStarting port cannot be greater than final port.\nPlease try again.")
        continue
    if user_port_start < 1 or user_port_end < 1:
        print("\nPorts cannot be less than 1.\nPlease try again.")
        continue
    if user_port_start > 65535 or user_port_end > 65535:
        print("\nPorts cannot be greater than 65535.\nPlease try again.")
        continue

    working = True #This is used to end loading function when this variable becomes false
    loader = threading.Thread(target=loading)  #Creates loader object as a second thread in background
    loader.start() #Begins the loading function

    start = time.time() #Records start time of scan

    port_values = {} #Dictionary used for recording each port and whether open or closed
    for port_no in range(user_port_start, user_port_end + 1): #Defines range, one added to end port to make inclusive
        if port_scan(user_ipv4, port_no, user_timeout): #Passes parameters to port_scan function, returns true or false
            port_values[port_no] = "Open" #Returns true, port number is assigned Open
        else:
            port_values[port_no] = "Closed" #Returns false, port number assigned false

    working = False #Stops the loading function
    loader.join()  #Program waits for loader function's thread to rejoin the main thread
    end = time.time() #Records end time of scan

    for item in port_values: #Every item in port dictionary, loops through keys
        print(f"Port {item}: {port_values[item]}") #Formats every element in dictionary
    print(f"Time taken: {end - start:.2f} seconds") #End - Start = How many seconds, :.2f formats to two decimal places

    try:
        instruction = input("Would you like to scan again?") #Breaks while loop if not y or yes
    except (ValueError, KeyboardInterrupt):
        print("Invalid input. Exiting...") #Incorrect input breaks loop
        break
    instruction = instruction.lower()
print("End of program.") #Only prints if loop breaks and program closes gracefully
