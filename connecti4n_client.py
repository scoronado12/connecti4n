# File:   connecti4n_client.py
# Author: Ethan Martin & Stefano Coronado
# Date:   28 March 2019
# Brief:  Client for a game of Connect I4n
#
# We hereby declare on our word of honor that we have neither given nor
# received any unauthorized help on this work.

import socket
import sys
VERSION = '1.0'

MSG_CODES = ['ERROR', 'STOP', 'START', 'MOVE', 'BOARD', 'RESULT']


def main():
    HOST = input("Welcome to Connect I4n!\nWhat is the server IP address? ")
    PORT = 4414


    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        print("Connected to " , HOST)
        start = input("Would you like to start the game? [y/n] ")
        if (start == 'y'):
            print("You are Token 1, server is token 2")
            # send start command to server
            c4n_send_start(sock)
            #winner = False #TODO maybe replace this with a detect winner packet from server

            while True:
                move_magic(sock)


                #winner = True #break loop while debugging

            # Game exits when exiting from loop
            sock.close()
            exit(0)
        else:
            sock.close()
            exit(0)
    except KeyboardInterrupt:
        sock.close()
    except ConnectionRefusedError:
         print("The server you are trying to connect to is not found")
         exit(1)
    sock.close()



def c4n_validate(data):
    # Decode the data
    lines = data.decode().split('\n')

    # Extract the header
    header = lines[0].split()
    
    # Validate length
    if (len(header) != 3 or
        header[0] != 'C4N' or
        header[1] != VERSION or
        header[2] not in MSG_CODES):
        print('Bad message')
        raise Exception

    # Read the content if present
    if len(lines) > 1:
        content = ''
        for l in lines[1:]:
            content += l
    else:
        content = None

    # Return results
    #print('Good message!')
    return header[2], content



# Send start command to server
def c4n_send_start(sock):
    out = "C4N " + VERSION + " " + MSG_CODES[2] + '\n'
    encOut = out.encode()
    sock.sendall(encOut)


# Send to server
def c4n_message(code, content):
    if code not in MSG_CODES:
        return None

    out = 'C4N ' + VERSION + ' ' + code

    if content != None:
        out += '\n' + str(content)
    #print(out) # uncomment to see what packet is going out
    return out.encode()


# Board Data
def board_unflatten(board_data):

    board = board_data [4:]
    board = [board[i:i+14] for i in range(0, len(board), 14)]
    print("A B C D E F G")
    for list in board:
        print(list)
    return board


## Turns the user's selection into a proper char that the server can read
def letterInNumOut(moveLetter):
    number_letter = dict(zip(['A', 'B', 'C', 'D', 'E', 'F', 'G'], [0, 1, 2, 3, 4, 5, 6]))
    for num in number_letter:
        numOut = number_letter[moveLetter]
        #print(numOut)
        return numOut

    print('Invalid move')
    return None

def move_magic(sock):
    print("AI Turn")
    recieve_packet = sock.recv(1024) #get board/error/result from server
    whatIs_recieve = c4n_validate(recieve_packet)
    #print(recieve_packet)
    if (whatIs_recieve[0] == 'BOARD'):
        current_board = board_unflatten(whatIs_recieve[1]) #This is a list
        move = input("Which is your move? (Enter A-F) ") #take the move

        move = letterInNumOut(move)
        #send Move Packet back

        sock.sendall(c4n_message('MOVE', move))
        # recieve is valid packet


    elif (whatIs_recieve[0] == 'ERROR'):
        
        if int(whatIs_recieve[1]) == 2:
            print("Bad Move")
            move = input("Which is your move? ") #take the move

            move = letterInNumOut(move)
            #send Move Packet back

            sock.sendall(c4n_message('MOVE', move))
            
        else:
            print("Unknown Error")
            raise KeyboardInterrupt

    elif (whatIs_recieve[0] == 'RESULT'):

        if whatIs_recieve[1] == '1':
            print("You Win!\nConnect I4n!")
            sock.close()
            exit()
        elif whatIs_recieve[1] == '2':
            print("You Lose!\nConnect I4n!")
            sock.close()
            exit()





main()
