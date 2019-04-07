# File:   connecti4n_client.py
# Author: Ethan Martin & Stefano Coronado
# Date:   28 March 2019
# Brief:  Client for a game of Connect I4n
#
# We hereby declare on our word of honor that we have neither given nor
# received any unauthorized help on this work.

import socket

VERSION = '1.0'

MSG_CODES = ['ERROR', 'STOP', 'START', 'MOVE', 'BOARD', 'RESULT']

# Send start command to server
def c4n_send_start(sock):
    out = 'C4N ' + VERSION +' ' + MSG_CODES[2]
    sock.sendall(out.encode())


# Send to server
def c4n_send_msg(codigo, contenido, sock):
    #make sure there is a valid code
    if (codigo not in  MSG_CODES ):
        return None
    else:
        # construct basic message
        out = 'C4N ' + VERSION + ' ' + codigo
        # append content if there is anything on the 
        if (contenido != None):
            out += '\n' + str(contenido)
        print(out)
        #send all generated headers
        sock.sendall(out.encode())

def c4n_get_msg(sock):
    #TODO pass back a string containing the value of out from server

    msg = sock.recv(1024)

    return msg.decode()

def main():
    HOST = input("Welcome to Connecti4n!\nWhat is the server IP address? ")
    PORT = 4414


    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        start = input("Would you like to start the game?")
        if (start == 'y'):
            while True:
                message_to_server = input("Test a message ")
                #as is it will pass in the start command
                #c4n_send_msg(MSG_CODES[2], message_to_server, sock)
                message_from_server = c4n_get_msg(sock)
                print(message_from_server)
        else:
            exit(0)
    except (KeyboardInterrupt):
        sock.close()
    except ConnectionRefusedError:
         print("The server you are trying to connect to is not found")
         exit(1)
    sock.close()

main()
