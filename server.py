__author__ = 'ratijha'
import socket
from threading import *


class ServerSocket(object):

    def __init__(self):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind(('localhost', 12345))
        self.serversocket.listen()
        self.client_threads = []
        # self.listen()

    def recv_msg(self, conn, addr ):
        conn.send("Welcome to the Chat Room".encode('utf-8'))
        while True:
            try:
              message = conn.recv(100)
              if message:
                  """prints the message and address of the
                                      user who just sent the message on the server
                                      terminal"""
                  print("<" + addr[0] + "> " + message)

                  # Calls broadcast function to send message to all
                  message_to_send = "<" + addr[0] + "> " + message
                  self.broadcast(message_to_send, conn)

              else:
                  """message may have no content if the connection
                  is broken, in this case we remove the connection"""
                  self.remove(conn)

            except:
                continue
            # print('Got connection from', address)
            # conn.send('Thank you for connecting'.encode('utf-8'))
            # conn.close()

    def listen(self):
        while 1:
            #accept connections from outside
            (conn, address) = self.serversocket.accept()
            self.client_threads.append(conn)
            print("{0} Connected".format(address))
            th = Thread(self.recv_msg(conn, address))
            th.start()
        conn.close()
        self.serversocket.close()

    def broadcast(self, message, conn):
        for client in self.client_threads:
            if client != conn:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    client.close()

                    # if the link is broken, we remove the client
                    self.remove(client)

    def remove(self, conn):
        if conn in self.client_threads:
            self.client_threads.remove(conn)


ss = ServerSocket()
ss.listen()