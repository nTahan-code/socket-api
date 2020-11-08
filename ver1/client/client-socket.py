import socket
import sys
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
    print("My chat Room Client. Version One.")
    print("Commands: login, send, logout, newuser")
    #Ask the user what they want to do
    #Result code list:
    # -1 : user has not logged on to server
    # 0 : user has logged onto the server
    result_Code = -1 #User has not connected to server

    try:
        sobj.connect(IP_ADDRESS, PORT)
    except:
        print("Unable to connect to server")
        exit()

    while True:
        try:
            usr_input = input("")
            result_Code = menu(result_Code, usr_input)
        except:
            print("An error has occured")
    
    sobj.close()


#Checks the input of the user
def menu(result_Code, usr_input):
    parse_string = usr_input.split()[0]
    if(parse_string=="login"):
        if(result_Code == -1):
            test_var = login(usr_input().split[1], usr_input().split[2])
            if(test_var==1):
                return 0 #User has successfully logged onto the server
            else:
                return -1 #User was unable to log onto the server, function login will display error
        else:
            print("ERROR: User is already logged in")
            return -1
    elif(parse_string =="newuser"):
        test_var = new_user(usr_input().split[1], usr_input().split[2])
        if(test_var==1):
            return 0 #User has successfully made a new user
        else:
            return -1 #User was unable to make a new user
    elif(parse_string == "send"):
        if(result_Code ==-1):
            print("Error: You must login first!")
        else:
            test_var = send_msg(usr_input)
            if(test_var==1):
                return 0 #User has successfully sent a message
            else:
                return 0 #User was unable to send a message, Error message will be displayed in send function
    elif(parse_string == "logout"):
        if(result_Code == 0):
            logout()
            return -1
        else:
            print("You are already logged out!")
            return -1
    else:
        print("Error unknown command!")
        return result_Code


def send_msg(usr_input):
    message = usr_input.split('',1)
    sobj.sendall(message)



#Login to the server by passing userID and password, will return error if unable to login
def login(userID, password):
    
    sobj.send(userID,password)
    result_Code = 

#Creates new user
def new_User(userID, password):
    if(len(UserID)>32):
        print("Error UserID is too long. UserID must be less than 32 characters")
        return -1
    elif(len(password)<4 or len(password)>8):
        print("Error: Password must be between 4 and 8 characters in length")
        return -1
    else:

#Call main
main()