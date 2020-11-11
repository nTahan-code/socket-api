#Nicholas Tahan, November 11, 2020
#Server Version Two:
#This program will connect to several clients at once and send data between them
#When a new user connects to the server a new thread is created
#The user can select from the following commands:
# 1. who - server returns a list of logged in users
# 2. send all - Server sends a message to all connected users
# 3. send userID - Server sends a message only to the user with userID specified
# 4. login user_name password - server checks to see if account exists, if it does let the user login
# 5. logout - If the user is logged in, let them log out. Disconnect from the server
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

global clientList
clientList = [] #List keeps track of client connections


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
    global clientList
    NumClient = NumClient+1
    clientList.append(connection)

    while connected:
        c_input = receive_Client_data(connection)
        print(c_input)
        msg_length = len(c_input.split())
        #Outside if statements test for commands
        if(msg_length >= 1):
            if(c_input.split()[0]=="login"):
                if(logged_in == False):
                    if(msg_length ==3):
                        name=usr_login(c_input.split()[1], c_input.split()[2])
                        if(name == "null"):
                            print("Unable to login")
                            connection.sendall("Error, unable to login. Please verify user login actually exists! Or is not already logged onto server!".encode("utf8"))
                        else:
                            logged_in=True
                            connection.sendall(("Successfully logged in as "+ c_input.split()[1]).encode("utf8"))#Notifies user they were successfully logged in
                            user_name = c_input.split()[1]
                            pure_msg(connection, (user_name+" entered the chat."))
                            print(user_name + " login")
                            hostconnection[user_name] = connection #Sets the connection as the value for the key user_name
                    else:
                        connection.sendall("Invalid amount of arguments sent!".encode("utf8"))
            
            elif(c_input.split()[0]=="send"):
                if(logged_in==True): #Tests if sender is logged into server
                    if(msg_length > 2): #Tests to see if sender specified command, person to send to and actual message
                        if(c_input.split()[1] in hostconnection): #Tests to see if receiver userID is actually connected to server
                            send_PM(connection, c_input.split()[1], user_name, c_input)
                        elif(c_input.split()[1]== "all"):
                            send_msg(connection, c_input, user_name)
                        else:
                            connection.sendall((c_input.split()[1]+" is not connected to server!").encode("utf8"))
                    else:
                        connection.sendall("You must send an actual message!".encode("utf8"))
                else:
                    connection.sendall("You must be logged in to send messages".encode("utf8"))
            
            elif(c_input.split()[0]=="logout"):
                if(logged_in== True):
                    try:
                        pure_msg(connection,(user_name+ " left the chat.")) #Informs the rest of the clients that a user disconnected
                        connection.sendall(("Logging out user "+ user_name).encode("utf8")) #Sends a message to the user logging out that the server logged them out
                        del hostconnection[user_name] #Removes connection from dictionary
                        clientList.remove(connection)
                        connection.close() #Closes connection with client
                        connected = False
                        NumClient = NumClient-1 #Decrement number of clients connected
                        print(user_name + " logout")
                    except Exception as error:
                        print("Error: ", error)
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
                        #Only triggers if user sends an incorrect number of arguments
                        connection.sendall("Invalid amount of arguments sent!".encode("utf8"))
            elif(c_input.split()[0]=="who"):
                who(connection)
                print("who")
            else:
                print("Unkown command...")

#Sends a pure message, no string manipulation. Used for login and logout
def pure_msg(connection, message):
    global clientList
    try:
        for conn in clientList:
            if connection != conn:
                conn.sendall(message.encode("utf8"))
    except Exception as error:
        print("Error: ", error)

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


#Sends a private message from one user to another
def send_PM(connection, recieverUserName, senderUserName, message):
    message = message.split(' ',1)[1] #Removes the word send from the message
    message = message.split(' ',1)[1] #Removes the recieverID from the message
    string = "(" + senderUserName + " to " + recieverUserName + ") " + message #Append sender user name ' to ' and receiverusername to the message
    print(string)
    try:
        hostconnection[recieverUserName].sendall(string.encode("utf8"))
    except Exception as error:
        print("Error: ", error)

#Iterates through dictioanry and sends the message to all connected users, except the user who sent the message
def send_msg(connection, message, userName):
    global clientList
    message = message.split(' ',1)[1] #Removes the word send from the message
    message = message.split(' ',1)[1] #Removes the recieverID from the message
    string = userName + ": " + message
    print(string)
    try:
        for conn in clientList:
            if connection != conn:
                conn.sendall(string.encode("utf8"))
    except Exception as error:
        print("Error: ", error)

#Tests to see if user_name already exists. If it does not create a new user account
def new_user(user_name, password):
    dictionary = get_dictionary()
    if user_name in dictionary:
        return "null"
    else:
        append_User(user_name, password)
        return user_name
        print("Successfully created new user")

#Append the user account to the end of users.txt file
def append_User(user_name, password):
    #Try statements are used in case file is not found
    try:
        filePtr = open("users.txt","a")
        filePtr.write(user_name + " " + password + " \n")
        filePtr.close()
    except Exception as error:
        print("Error: ", error)

#Checks to see if there is a user account that matches the user_name and password
def usr_login(user_name, password):
    dictionary = get_dictionary()
    print(dictionary)
    if(user_name in hostconnection):
        return 'null'
        if user_name in dictionary:
            reference_password = dictionary[user_name]
            if(reference_password == password):
                return user_name
            else:
                return "null"
        return "null"

#Returns a dictionary that has key: userID and value: password. This dictionary holds all the items in users.txt
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

#This function receives data from the client.
def receive_Client_data(connection):
    c_input = connection.recv(MAX_BUFFER_SIZE)
    c_input_length = sys.getsizeof(c_input)

    if(c_input_length > MAX_BUFFER_SIZE):
        print("The size received is greater than Max allotted size") 

    decode_input = c_input.decode("utf-8").rstrip() #Transfers the input into readable text

    return decode_input

main()