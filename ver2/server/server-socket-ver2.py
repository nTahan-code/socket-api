import socket
import sys
import traceback
from threading import Thread

IP = '127.0.0.1'
PORT = 12483
MAX_BUFFER_SIZE = 1024
hostconnection = {} #Key wil be connection, value will be userID
global MAXCLIENTS #maximum number of clients allowed to connect
MAXCLIENTS = 3
global NumClient #Keeps track of number of connected clients
NumClient = 0

def main():

    sobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sobj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    #Create Socket object

    try:
        sobj.bind((IP,PORT))
    except:
        print("Could not bind to port:",PORT)
        sys.exit()

    sobj.listen(8) #Will listen up to 8

    print("Chat room Version 2 server up and running!")

    while True:
        conn, address = sobj.accept() #Get the connection object and the address used by the client
        try:
            if(NumClient < MAXCLIENTS):
                Thread(target=client_connect, args=(conn,address)).start() #Creates thread for each client
            #client_connect(conn, address)
        except Exception:
            print("Error: ", traceback.format_exc())
    sobj.close()

def client_connect(connection, address):
    connected = True
    logged_in = False
    name = "null"
    user_name = ""
    global NumClient
    NumClient = NumClient+1

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
                        hostconnection[user_name] = connection #Sets the connection as the value for the key user_name
                else:
                    connection.sendall("Invalid amount of arguments sent!".encode("utf8"))
        elif(c_input.split()[0]=="send" and c_input.split()[1]=="all"):
            if(logged_in== True):
                if(msg_length > 1):
                     send_msg(connection, c_input, user_name)
                else:
                    connection.sendall("You must send an actual message!".encode("utf8"))
            else:
                connection.sendall("You must be logged in to send messages".encode("utf8"))
        elif(c_input.split()[0]=="send"):
            if(logged_in==True): #Tests if sender is logged into server
                if(msg_length > 2): #Tests to see if sender specified command, person to send to and actual message
                    if(c_input.split()[1] in hostconnection.values()): #Tests to see if receiver userID is actually connected to server
                        send_PM(connection, c_input.split()[1], c_input)
                    else:
                        connection.sendall(c_input.split()[1]+" is not connected to server!".encode("utf8"))
                else:
                    connection.sendall("You must send an actual message!".encode("utf8"))
            else:
                connection.sendall("You must be logged in to send messages".encode("utf8"))
        elif(c_input.split()[0]=="logout"):
            if(logged_in== True):
                connection.sendall("Logging out user"+ user_name.encode("utf8"))
                del hostconnection[user_name] #Removes connection from dictionary
                connection.close() #Closes connection with client
                connected = False
                NumClient = NumClient-1
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
        elif(c_input.split()[0]=="who"):
            who(connection)

#Determines who is connected, sends a list of connected users back to the client
def who(connection):
    userList = []
    for userID in hostconnection:
        userList.append(userID) #creates a list of all user IDs connected to the server
    try:
        if not userList: #If no one is logged into the server, However people can be connected, but not logged in and still will not show up!
            connection.sendall("No one is connected to the server".encode("utf8"))
        else:
            connection.sendall(str(userList).encode("utf8")) #Sends list of IDs back to user
    except Exception as error:
        print("Error: ", error)



def send_PM(connection, recieverUserName, message):
    message = message.split(' ',1)[1] #Removes the word send from the message
    message = message.split(' ',1)[1] #Removes the recieverID from the message
    string = "(" + hostconnection[connection] + " to " + recieverUserName + ") " + message #Append sender user name ' to ' and receiverusername to the message
    try:
        hostconnection[recieverUserName].sendall(string.encode("utf8"))
    except Exception as error:
        print("Error: ", error)

#Iterates through dictioanry and sends the message to all connected users, except the user who sent the message
def send_msg(connection, message, userName):
    string = userName + ": " + message.split(' ',1)[1] #Removes the send command, and append username to start of message
    try:
        for conn in hostconnection.values():
            if connection != conn:
                conn.sendall(string.encode("utf8"))
    except Exception as error:
        print("Error: ", error)

def new_user(user_name, password):
    dictionary = get_dictionary()
    print(dictionary)
    if user_name in dictionary:
        return "null"
    else:
        append_User(user_name, password)
        return user_name
        print("Successfully created new user")

def append_User(user_name, password):
    try:
        filePtr = open("users.txt","a")
        filePtr.write(user_name + " " + password + " \n")
        filePtr.close()
    except Exception as error:
        print("Error: ", error)

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


def receive_Client_data(connection):
    c_input = connection.recv(MAX_BUFFER_SIZE)
    c_input_length = sys.getsizeof(c_input)

    if(c_input_length > MAX_BUFFER_SIZE):
        print("The size received is greater than Max allotted size") 

    decode_input = c_input.decode("utf-8").rstrip() #Transfers the input into readable text

    return decode_input

main()