# File:   connecti4n_client.py
# Author: Ethan Martin & Stefano Coronado
# Date:   28 March 2019
# Brief:  Client for a game of Connect I4n
#
# We hereby declare on our word of honor that we have neither given nor
# received any unauthorized help on this work.

import socket

VERSION = '1.0'

# Send to server
def c4n_send_msg(codigo, contenido):
    #make sure there is a valid code
    if (codigo not in  ['ERROR', 'STOP', 'START', 'MOVE', 'BOARD', 'RESULT']):
        return None
    
    # construct basic message
    
    out = 'C4N ' + VERSION + ' ' + code
    
    # append content if there is anything
    
    if (content != None):
        out += ' ' + str(content)
    
    #return generated headers
    
    return out.encode()
    
def c4n_get_msg(sock):
    #TODO pass back a string containing the value of out from server
    
    
    msg = sock.recv(1024)
    
    return msg.decode()
    


def main():
    HOST = 'localhost'
    PORT = 4414

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    sock.connect((HOST, PORT))
    
    message_from_server = c4n_get_msg(sock)
    
    print(message_from_server)
        
        
    
    sock.close()
    
    

main()
