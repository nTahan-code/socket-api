#Nicholas Tahan, November 11, 2020
#Client Version Two:
#This program will connect to a server already running. It will create a new thread to listen for feeback from the server.
#The client will also accept input while receiving feedback from the server
#Multiple instances of this client can connect to the server
#The user can select from the following commands:
# 1. who - server returns a list of logged in users
# 2. send all - Server sends a message to all connected users
# 3. send userID - Server sends a message only to the user with userID specified
# 4. login user_name password - server checks to see if account exists, if it does let the user login
# 5. logout - If the user is logged in, let them log out. Disconnect from the server
import socket
import sys
import select
import traceback
import time
from threading import Thread
#Port Number: 12483
#Threads are used to allow the client to search for receiving data and to wait for user input at the same time

PORT = 12483 #define port constant
IP_ADDRESS = '127.0.0.1' #Define IP address

global logged_In
logged_In = False

global User_ID
User_ID = ''
global output
output = ""

global keepThread
keepThread=True#Kills the thread when user logs out

try:
    sobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create port object
except:
    print("Socket failed to create")
    sys.exit()


def main():
    global logged_In
    global keepThread
    logged_In = False
    print("My chat Room Client. Version Two.")
    print("Commands: login, send all, send UserID, logout, newuser, who")
    #Ask the user what they want to do

    try:
        sobj.connect((IP_ADDRESS, PORT))
        sobj.settimeout(2)#Sets timeout for listening
    except:
        print("Unable to connect to server")
        exit()
    
    Thread(target=listen_for_data, args=()).start() #Creates new thread to listen for data from the server

    while True:
        try:
            if(keepThread==True):
                usr_input = input("--> ")
                logged_In = menu(usr_input, logged_In)
            else:
                break

        except Exception as error:
            if(error.args[0]!="timed out"):
                print("Error: ", error)
        except OSError as err:
            print("Lost connection to server")
            keepThread = False
            break

    
    sobj.close()

#Thread actively listens for data from the server
def listen_for_data():
    global output
    global keepThread
    while keepThread:
        try:
            msg = sobj.recv(2048).decode("utf8")
            output = msg
            print(msg)#If server sends data, prints the data to the screen
        except Exception as error:
            if(error.args[0]!="timed out"):
                    print("Error: ", error)
        except OSError as err:
            print("lost connection to server")
            keepThread = False

#sends client input to server
def send_msg(usr_input):
    sobj.sendall(usr_input.encode("utf8"))

#Sends logout to server and logs out the user
def logout(user_name):
    global logged_In
    global keepThread
    keepThread = False
    sobj.sendall("logout".encode("utf8"))
    time.sleep(2)
    msg = output
    if msg== ("Logging out user "+user_name):
        logged_In = False
        print("Successfully logged out")

#Login to the server by passing userID and password, will return error if unable to login
def login(userID, password, usr_input):
    global output
    global User_ID
    User_ID = userID
    sobj.send(usr_input.encode("utf8"))
    time.sleep(2) #Waits for the server to respond
    msg = output
    if "Error" in msg:
        return False
    else:
        return True

#Checks the user input to see if new account is valid. From there if all the information is valid, it will send the data to the server.
#The server will check to see if the account already exists. If it does it will not allow a new account to be made. If it does not a new account will be made.
def new_User(userID, password, usr_input):
    if(len(userID)>32):
        print("Error UserID is too long. UserID must be less than 32 characters")
        return -1
    elif(len(password)<4 or len(password)>8):
        print("Error: Password must be between 4 and 8 characters in length")
        return -1
    else:
        sobj.sendall(usr_input.encode("utf8"))
        

#Checks the input of the user, it checks the first word of the input. The first word dictates a command
def menu(usr_input, logged_In):
    global User_ID
    parse_string = usr_input.split()[0]
    wordCount = len(usr_input.split()) #Ensures the user enters in the correct amount of arguments

    #User must not already be logged in to login
    if(parse_string=="login"):
        if(logged_In == False):
            logged_In = login(usr_input.split()[1], usr_input.split()[2], usr_input)
                
        else:
            print("ERROR: User is already logged in")
    elif(parse_string =="newuser"):
        if(logged_In == False):
            if(wordCount==3):
                new_User(usr_input.split()[1], usr_input.split()[2], usr_input)
            else:
                print("Incorrect number of arguments!")
        else:
            print("Error: Must be logged out to create new account")
    #send all and send userID are both sent through here
    elif(parse_string == "send"): #Send works for both send all and send user, the server will actually differentiate between them
        if(logged_In ==False):
            print("Error: You must login first!")
        else:
            send_msg(usr_input)
    
    elif(parse_string == "logout"):
        if(logged_In == True):
            logout(User_ID)
        else:
            print("You are already logged out!")
    #The client just sends who to the server
    elif(parse_string == "who"):#Can reuse the send_msg function since the server will handle the actual response
        send_msg(usr_input)

    else:
        print("Error unknown command!")
    return logged_In


        

#Call main
main()