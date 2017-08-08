__author__ = 'ratijha'
import socket
import select
import sys

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 12345))

# clientsocket.connect((host, port))
# print(clientsocket.recv(1024))
# clientsocket.close()

while True:

    # maintains a list of possible input streams
    sockets_list = [sys.stdin, clientsocket]
    # print(sockets_list)
    """ There are two possible input situations. Either the
    user wants to give  manual input to send to other people,
    or the server is sending a message  to be printed on the
    screen. Select returns from sockets_list, the stream that
    is reader for input. So for example, if the server wants
    to send a message, then the if condition will hold true
    below.If the user wants to send a message, the else
    condition will evaluate as true"""
    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])

    for socks in read_sockets:
        if socks == clientsocket:
            message = socks.recv(2048)
            print(message)
        else:
            message = sys.stdin.readline()
            clientsocket.send(message.encode('utf-8'))
            sys.stdout.write("<You>")
            sys.stdout.write(message)
            sys.stdout.flush()
clientsocket.close()
      # Close the socket when done