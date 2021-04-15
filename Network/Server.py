import pickle
import socket

# create socket and initalize connection type
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# get hostname of Network server is on
hostname = socket.gethostname()
print(hostname)
# use hostname to get ipaddress
ip_address = socket.gethostbyname(hostname)
# bind socket to port and ip address
print(ip_address)
serversocket.bind(('127.0.0.1', 5001))

# listen for connections
serversocket.listen()

# list of connections
connection = []

# wait for two clients to connect before we start the game
def waiting_for_connections():
    while len(connection) < 2:
        conn, addr = serversocket.accept()
        connection.append(conn)
        print(conn)
        print(connection)


# unpickle data from client
def recieve_information():
    player_1_info = pickle.loads(connection[0].recv(1024))
    player_2_info = pickle.loads(connection[1].recv(1024))

    return player_1_info, player_2_info


waiting_for_connections()
# main server loop
while True:

    player1, player2 = recieve_information()
    print(player1)
    print(player2)
    message = "hello dudes"
    data_arr = pickle.dumps(message)
    # print(data_arr)
    connection[0].send(data_arr)
    connection[1].send(data_arr)


