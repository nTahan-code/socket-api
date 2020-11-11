#Nicholas Tahan, November 11, 2020
#Server Version one:
#This server will connect to a client. Only one client can be connected to the server at a single time
#The user can enter the following commands:
# 1. login UserID, password - logs in the user, assuming the account already exists and the userID and password match
# 2. logout - logs the user out of the server, disconnects from the server
# 3. newuser userID password- creates a new user account, assuming the userID is not already taken
# 4. send [message here] - send a message to the server
import socket
import sys
import traceback

IP = '127.0.0.1'
PORT = 12483
MAX_BUFFER_SIZE = 1024

def main():

    sobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sobj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #TEST THIS FUNCTION MORE
    #Create Socket

    try:
        sobj.bind((IP,PORT))
    except:
        print("Could not bind to port:",PORT)
        sys.exit()

    sobj.listen(8)

    print("Chat room Version 1 server up and running!")

    while True:
        conn, address = sobj.accept() #Get the connection object and the address used by the client
        try:
            client_connect(conn, address)
        except Exception as error:
            print("Error: ", error)
    sobj.close()

#
def client_connect(connection, address):
    connected = True
    logged_in = False
    name = "null"
    user_name = ""
    while connected:
        c_input = receive_Client_data(connection)
        print(c_input)
        msg_length = len(c_input.split())
        #Outside if statements test for commands
        if(c_input.split()[0]=="login"):
            if(logged_in == False):
                if(msg_length ==3):
                    name=usr_login(c_input.split()[1], c_input.split()[2])
                    if(name == "null"):
                        print("Unable to login")
                        connection.sendall("Error, unable to login. Please verify user login actually exists!".encode("utf8"))
                    else:
                        logged_in=True
                        connection.sendall(("Successfully logged in as "+ c_input.split()[1]).encode("utf8"))
                        user_name = c_input.split()[1]
                else:
                    connection.sendall("Invalid amount of arguments sent!".encode("utf8"))

        elif(c_input.split()[0]=="send"):
            if(logged_in== True):
                string = user_name + ": " + c_input.split(' ',1)[1] #Appends username and user msg
                connection.sendall(string.encode("utf8"))
            else:
                connection.sendall("You must be logged in to send messages".encode("utf8"))
                
        elif(c_input.split()[0]=="logout"):
            if(logged_in== True):
                connection.sendall("Logging out user".encode("utf8"))
                connection.close()
                connected = False
            else:
                connection.sendall("Error! User must be logged in before logging out".encode("utf8"))

        elif(c_input.split()[0]=="newuser"):
            if(logged_in==False):
                if(msg_length==3):
                    testvar = new_user(c_input.split()[1], c_input.split()[2]) #Calls the new user function, checks to see if user already exists
                    if(testvar=="null"):
                        connection.sendall("Error! User account was unable to be created".encode("utf8"))
                    else:
                        connection.sendall("User account successfully created!".encode("utf8"))
                else:
                    connection.sendall("Invalid amount of arguments sent!".encode("utf8"))
                

#Creates a new user, assuming user_name is not already taken
def new_user(user_name, password):
    dictionary = get_dictionary() #get_dictionary() returns a dictionary with all logins
    print(dictionary)
    if user_name in dictionary:
        return "null" #Username already exists
    else:
        append_User(user_name, password)
        return user_name #Account was successfully created
        print("Successfully created new user")

#append_user() actually adds the user to the users.txt file
def append_User(user_name, password):
    try:
        filePtr = open("users.txt","a")
        filePtr.write(user_name + " " + password + " \n")
        filePtr.close()
    except Exception as error:
        print("Error: ", error)

#usr_login will log in the user, assuming account exists, and userID and password match and existing account
def usr_login(user_name, password):
    dictionary = get_dictionary()
    print(dictionary)
    if user_name in dictionary:
        reference_password = dictionary[user_name]
        if(reference_password == password):
            return user_name
        else:
            return "null"
    return "null"

#returns a dictionary full of all user account information
def get_dictionary():
    try:
        filePtr = open("users.txt","r")
        dictionary = {} #Stores the usernames and passwords in a dictionary

        for line in filePtr:
            dictionary[line.split()[0]] = line.split()[1]
        
        filePtr.close()
    except Exception as error:
        print("Error: ",error)

    return dictionary

#Gets the client data
def receive_Client_data(connection):
    c_input = connection.recv(MAX_BUFFER_SIZE)
    c_input_length = sys.getsizeof(c_input)

    if(c_input_length > MAX_BUFFER_SIZE):
        print("The size received is greater than Max allotted size") 

    decode_input = c_input.decode("utf-8").rstrip() #Transfers the input into readable text

    return decode_input

main()