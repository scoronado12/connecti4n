# ConnectI4n

A simple Connect 4 server and client for CPSC 414.

# Protocol

Each message passed between a client and a server must have at least three
components, separated by a space. First, `C4N` to signify that this is a
ConnectI4n message. Next, a version number. Finally, the message type.
Available message types are determined by the protocol version. Some message
types may have additional data following the header, separated by a newline
character. The format of this data is expected to be known to the
client/server.

## Message Types

### Version 1.0

| Message Type | Data Length | Direction        |
| ---          | ---         | ---              |
| ERROR        | 1           | any              |
| STOP         | none        | any              |
| START        | none        | client -> server |
| MOVE         | 1           | client -> server |
| BOARD        | variable    | server -> client |
| RESULT       | 1           | server -> client |


#### `ERROR`

Error messages can be sent from either the client or the server at any time to
indicate that something has gone wrong. A single number is allowed as data,
signifying the error code. Available codes are as follows:

| Error | Description                          |
| ---   | ---                                  |
| 1     | Invalid message                      |
| 2     | (server -> client only) Invalid move |
| 3     | (server -> client only) Server full  |
| 99    | Unknown error                        |


#### `STOP`

The client or the server can cleanly attempt to close the game early using this
message. A client or server need not respond to this message, and may terminate
the connection immediately.


#### `START`

A client wishing to begin a new game opens a connection and sends this message.
If the server is full, it will respond with error code 3 and a game will not
begin. Otherwise the server will respond with the initial board state.


#### `MOVE`

When it is the player's turn, the client should prompt the user for the column
in which they would like to place a token, and send the integer index of that
column as the data for this message. If it is not possible to place a token
where the player has chosen, the server will respond with error code 2. A
responsible client should however check the validity of the move before sending
to the server. If the move is valid, the server will respond with two `BOARD`
messages: one after the player's move, and another after the AI's move.


#### `BOARD`

The server uses this message to communicate the current state of the game board
to the client. It will have at minimum two integer parameters, one with the
number of columns, and another with the number of rows. The current value for
each space on the board will follow in sequence row by row, where `0` is an 
empty space, `1` is a player token, and `2` is an AI token:

#### `RESULT`

When the game has ended as a result of normal play, the server sends this
message to inform the client of the winner. The data will be a `1` if the
player wins, and a `2` if the AI wins. At this point the connection will be
terminated.

