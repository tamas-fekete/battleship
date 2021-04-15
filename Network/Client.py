"""
This is the client file and will send button press signals from both paddles to the server for calculations.
The client file recieves the positions of the ball and both players from the server.
The client file also draws everything on the screen.
"""

import pickle
import socket


# get host name of wifi computer is connected too
# hostname = socket.gethostname()
# ip_address = socket.gethostbyname(hostname)

# recieve and unpickle data from server
def receive_data():
    data = clientsocket.recv(1024)
    data = pickle.loads(data)

    return data


# main game loop
def main():
    while True:
        message = input()
        data_arr = pickle.dumps(message)
        clientsocket.send(data_arr)

        info = receive_data()
        print("I. received from server: " + info)

        info = receive_data()
        print("II. received from server: " + info)

# create connection to server socket
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('127.0.0.1', 5001))

print("connection successfull, client 1 to server")

main()
