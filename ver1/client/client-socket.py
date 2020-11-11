#Nicholas Tahan, November 11, 2020
#Client Version one:
#This client will connect to a server. Only one client can be connected to the server at a single time
#The user can enter the following commands:
# 1. login UserID, password - logs in the user, assuming the account already exists and the userID and password match
# 2. logout - logs the user out of the server, disconnects from the server
# 3. newuser userID password- creates a new user account, assuming the userID is not already taken
# 4. send [message here] - send a message to the server
import socket
import sys
import select
#Port Number: 12483

PORT = 12483 #define port constant
IP_ADDRESS = '127.0.0.1' #Define IP address

global endSession
endSession = False #keeps track if the user wants to disconnect from the server

User_ID = ''

try:
    sobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create port object
except:
    print("Socket failed to create")
    sys.exit()


def main():
    logged_In = False
    print("My chat Room Client. Version One.")
    print("Commands: login, send, logout, newuser")

    try:
        sobj.connect((IP_ADDRESS, PORT)) #connects to the server
        sobj.settimeout(2) #sets server timeout
    except:
        print("Unable to connect to server")
        exit()

    #While loop will accept input from the user and try to receive user data.
    while True:
        try:
            usr_input = input("--> ") #Gets input from the user
            logged_In = menu(usr_input, logged_In)
            msg = sobj.recv(2048).decode("utf8")
            print(msg)

            if(endSession == True):
                print("Ending program")
                break
        except Exception as error:
            if(error.args[0]!="timed out"):
                print("Error: ", error)
    
    sobj.close()

#Sends a message to the server
def send_msg(usr_input):
    sobj.sendall(usr_input.encode("utf8"))

#Logs the user out from the server
def logout():
    global endSession
    endSession = True #This will end the program
    sobj.sendall("logout".encode("utf8"))
    if sobj.recv(2048).decode("utf8")== "Logging out user":
        logged_In = False
        print("Successfully logged out")

#Login to the server by passing userID and password, will return error if unable to login
def login(userID, password, usr_input):
    sobj.send(usr_input.encode("utf8"))
    msg = sobj.recv(2048).decode("utf8")
    print(msg)
    if "Error" in msg:
        return False
    else:
        return True

#Creates new user, assuming all the error checking succeeds, and if userID is not already taken
def new_User(userID, password, usr_input):
    print("In new user")
    if(len(userID)>32):
        print("Error UserID is too long. UserID must be less than 32 characters")
        return -1
    elif(len(password)<4 or len(password)>8):
        print("Error: Password must be between 4 and 8 characters in length")
        return -1
    else:
        sobj.sendall(usr_input.encode("utf8"))
        

#Checks the input of the user
def menu(usr_input, logged_In):

    parse_string = usr_input.split()[0]
    wordCount = len(usr_input.split())
    print(wordCount)

    if(parse_string=="login"):
        if(logged_In == False):
            if(wordCount == 3):
                logged_In = login(usr_input.split()[1], usr_input.split()[2], usr_input)
                if(logged_In==True):
                    print("Successfully logged onto server")  
            else:
                print("Incorrect number of arguments")
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
            
    elif(parse_string == "send"):
        if(wordCount >= 2):
            if(logged_In ==False):
                print("Error: You must login first!")
            else:
                send_msg(usr_input)
        else:
            print("Incorrect number of arguments")
            
    elif(parse_string == "logout"):
        if(logged_In == True):
            logout()
        else:
            print("You are already logged out!")
    else:
        print("Error unknown command!")
    return logged_In
        

#Call main
main()