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
    while connected:
        c_input = receive_Client_data(connection)
        #Outside if statements test for commands
        if(final.split(0)=="login"):
            if(logged_in == False):
                name=usr_login(user_name, password)
                if(name == "Null"):
                    print("Unable to login")
                    

            else:
                print("User: ", user_name, " is already logged in!")


def usr_login(user_name, password):
    try:
        filePtr = open("users.txt","r")
        file_lines = filePtr.readlines()
        dictionary = {} #Stores the usernames and passwords in a dictionary

        for line in file_lines:
            dictionary[line.strip(0)] = line.strip(1)
        
        filePtr.close()
        if user_name in dictionary:
            reference_password = dictionary[user_name]
            if(reference_password == password):
                return user_name
            else:
                return "null"
            



def receive_Client_data(connection):
    c_input = connection.recv(MAX_BUFFER_SIZE)
    c_input_length = sys.getsizeof(c_input)

    if(c_input_length > MAX_BUFFER_SIZE):
        print("The size received is greater than Max allotted size") 

    decode_input = client_input.decode("utf-8").rstrip() #Transfers the input into readable text
    final = process_input(decode_input)

    return final

main()