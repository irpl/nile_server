# Python program to implement server side of chat room.
import os
import socket
from _thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  
HOST = ""
PORT = int(os.getenv("PORT"))
 
server.bind((HOST, PORT))
server.listen(5)
 
list_of_clients = []
 
def clientthread(conn, addr):
  print("XR Connected.")

  while True:
    try:
      message = conn.recv(2048)
      if message:
        print (message)
        message_to_send = message
        broadcast(message_to_send, conn)

      else:
        remove(conn)

    except:
        print("exp")
        continue
 
def broadcast(message, connection):
  for clients in list_of_clients:
    if clients!=connection:
      try:
        clients.send(message)
      except:
        clients.close()
        # if the link is broken, we remove the client
        remove(clients)
 
def remove(connection):
  if connection in list_of_clients:
    list_of_clients.remove(connection)

while True:
  conn, addr = server.accept()

  list_of_clients.append(conn)

  print (addr[0] + " connected")

  start_new_thread(clientthread,(conn,addr))    
 
conn.close()
server.close()