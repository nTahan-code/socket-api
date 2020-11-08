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
        sobj.bind(host,port)
    except:
        print("Could not bind to port:",PORT)
        sys.exit()

    sobj.listen(8)

    while True:
        conn, address = sobj.accept() #Get the connection object and the address used by the client
        try:
            client_connect(conn, address)
        except:
            print("Could not establish connection with the client")

def client_connect(connection, address):
    connected = True
    logged_in = False
    name = "null"
    user_name = ""
    while connected:
        c_input = receive_Client_data(connection)
        #Outside if statements test for commands
        if(c_input.split(0)=="login"):
            if(logged_in == False):
                name=usr_login(c_input.split(1), c_input.split(2))
                if(name == "null"):
                    print("Unable to login")
                    connection.sendall("Error, unable to login. Please verify user login actually exists!".encode("utf8"))
                else:
                    logged_in=True
                    connection.sendall("Successfully logged in as".encode("utf8"))
                    user_name = c_input.split(1)
        elif(c_input.split(0)=="send"):
            if(logged_in== True):
                string = user_name + " " + c_input.split(' ',1)[1] #Appends username and user msg
                connection.sendall(string.encode("utf8"))
            else:
                connection.sendall("You must be logged in to send messages".encode("utf8"))
        elif(c_input.split(0)="logout"):
            if(logged_in== True):
                connection.sendall("Logging out user".encode("utf8"))
                connection.close()
                connected = False
            else:
                connection.sendall("Error! User must be logged in before logging out".encode("utf8"))
        elif(c_input.split(0)=="newuser"):
            if(logged_in==False):
                testvar = new_user(c_input.split(1), c_input.split(2)) #Calls the new user function, checks to see if user already exists
                if(testvar=="null"):
                    connection.sendall("Error! User account was unable to be created".encode("utf8"))
                else:
                    connection.sendall("User account successfully created!".encode("utf8"))
                


def new_user(user_name, password):
    dictionary = get_dictionary()
    if user_name in dictionary:
        return "null"
    else:
        append_User(user_name, password)
        return user_name

def append_User(user_name, password):
    try:
        filePtr = open("users.txt","a")
        filePtr.write(user_name + " " + password)
        filePtr.close()
    except Exception as error:
        print("Error: ", error)

def usr_login(user_name, password):
    dictionary = get_dictionary()
    if user_name in dictionary:
        reference_password = dictionary[user_name]
        if(reference_password == password):
            return user_name
        else:
            return "null"
            
def get_dictionary():
    try:
        filePtr = open("users.txt","r")
        file_lines = filePtr.readlines()
        dictionary = {} #Stores the usernames and passwords in a dictionary

        for line in file_lines:
            dictionary[line.strip(0)] = line.strip(1)
        
        filePtr.close()
    except Exception as error:
        print("Error: ",error)

    return dictionary


def receive_Client_data(connection):
    c_input = connection.recv(MAX_BUFFER_SIZE)
    c_input_length = sys.getsizeof(c_input)

    if(c_input_length > MAX_BUFFER_SIZE):
        print("The size received is greater than Max allotted size") 

    decode_input = client_input.decode("utf-8").rstrip() #Transfers the input into readable text
    final = process_input(decode_input)

    return final

main()