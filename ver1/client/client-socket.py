import socket
import sys
import select
#Port Number: 12483

PORT = 12483 #define port constant
IP_ADDRESS = '127.0.0.1' #Define IP address


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
    #Ask the user what they want to do
    #Result code list:
    # -1 : user has not logged on to server
    # 0 : user has logged onto the server
    result_Code = -1 #User has not connected to server

    try:
        sobj.connect((IP_ADDRESS, PORT))
        sobj.settimeout(2)
    except:
        print("Unable to connect to server")
        exit()

    while True:
        try:
            usr_input = input("--> ")
            logged_In = menu(usr_input, logged_In)
            msg = sobj.recv(2048).decode("utf8")
            print(msg)

        except Exception as error:
            if(error.args[0]!="timed out"):
                print("Error: ", error)
    
    sobj.close()


def send_msg(usr_input):
    sobj.sendall(usr_input.encode("utf8"))

def logout():
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

#Creates new user
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
            logged_In = login(usr_input.split()[1], usr_input.split()[2], usr_input)
            if(logged_In==True):
                print("Successfully logged onto server")
                
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
        if(logged_In ==False):
            print("Error: You must login first!")
        else:
            send_msg(usr_input)
            
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