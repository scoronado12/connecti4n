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
        # TODO fail
        print('Bad message')
        return None

    # Read the content if present
    if len(lines) > 1:
        content = ''
        for l in lines[1:]:
            content += l
    else:
        content = None

    # Return results
    print('Good message!')
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

    return out.encode()


# Board Data
def board_unflatten(board_data):
    if board_data[0] != MSG_CODES[4]:
        print("Not a BOARD packet")
        return None
    else:
        board = board_data[1][4:]

        n = 14
        board = [board[i:i+n] for i in range(0, len(board), n)]
        print("A B C D E F G")
        for list in board:
            print(list)
        return board

def board_flatten(board):
    out = str(len(board)) +  ' ' + str(len(board[0]))
    for row in board:
        for col in row:
            out += ' ' str(col)

    return out

def update_board(board_list, move):

    return board




def main():
    HOST = 'localhost'#input("Welcome to Connecti4n!\nWhat is the server IP address? ")
    PORT = 4414


    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        start = input("Would you like to start the game? ")
        if (start == 'y'):
            # send start command to server
            c4n_send_start(sock)
            winner = False #TODO maybe replace this with a detect winner packet from server
            while winner != True:
                board_data = c4n_validate(sock.recv(1024)) #get board from server
                current_board = board_unflatten(board_data) #This is a list
                move = input("Which is your move? ") #take the move
                current_board = update_board(current_board, move) #update the board, returning the board as a list
                sock.sendall(c4n_message('BOARD', current_board)) #send it back
        else:
            sock.close()
            exit(0)
    except KeyboardInterrupt:
        sock.close()
    except ConnectionRefusedError:
         print("The server you are trying to connect to is not found")
         exit(1)
    sock.close()

main()
