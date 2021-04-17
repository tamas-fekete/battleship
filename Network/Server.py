import pickle
import socket
from gameLogic.PlayerState import PlayerState


class Server():
    def __init__(self):
        # create socket and initalize connection type
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # get hostname of Network server is on
        self.hostname = socket.gethostname()
        print(self.hostname)
        # use hostname to get ipaddress
        ip_address = socket.gethostbyname(self.hostname)
        # bind socket to port and ip address
        print(ip_address)
        self.serversocket.bind(('127.0.0.1', 5001))
        # listen for connections
        self.serversocket.listen()
        # list of connections
        self.connection = []

        self.player1 = PlayerState(gui=None, randomShips=False)
        self.player2 = PlayerState(gui=None, randomShips=False)

        self.waiting_for_connections()

    def initPlayerShips(self):

        player1GuiShips = self.player1.initShips()
        player2GuiShips = self.player2.initShips()

        data1 = pickle.dumps(player1GuiShips)
        self.connection[0].send(data1)

        data2 = pickle.dumps(player2GuiShips)
        self.connection[1].send(data2)

        # allow players to ask for new random ships

    def waiting_for_connections(self):

        while len(self.connection) < 1:  # while len(self.connection) < 2:
            conn, addr = self.serversocket.accept()
            self.connection.append(conn)
            print(conn)
            print(self.connection)

    def recieve_information(self):
        player_1_info = pickle.loads(self.connection[0].recv(1024))
        player_2_info = pickle.loads(self.connection[1].recv(1024))

        return player_1_info, player_2_info

    def startServer(self):
        # main server loop

        self.initPlayerShips()

        while True:
            # player1, player2 = recieve_information()

            guiShips = self.player1.initShips()
            guiShips = pickle.dumps(guiShips)
            self.connection[0].send(guiShips)

            ''' Szerver ötlet: 
            
            -for loop-ban vár 2 connection-ig a playerekre.
            -P1-nek küldi a hajókat, P2-nek küldi a hajókat
            
            while játék:
            - P1 től vár egy koordinátát.
            - P1 nek elküldi a resultot
            - P2 nek elküldi a resultot
            
            - P2-től vár egy koordinátát
            - P2-nek elküldi a resultot
            - P1-nek elküldi a resultot
            
            a result az a "radar" vagy az "ocean" grid
            
            '''






            # player_1_info = pickle.loads(self.connection[0].recv(1024))
            # print(player_1_info)
            #
            # message = "okay I got your message"
            # data_arr = pickle.dumps(message)
            # self.connection[0].send(data_arr)
            #
            # message = "client1 has sent me a message"
            # data_arr = pickle.dumps(message)
            # self.connection[1].send(data_arr)
            #
            # player_2_info = pickle.loads(self.connection[1].recv(1024))
            # print(player_2_info)
            #
            # message = "okay I got your message"
            # data_arr = pickle.dumps(message)
            # self.connection[1].send(data_arr)
            #
            # message = "client2 has sent me a message"
            # data_arr = pickle.dumps(message)
            # self.connection[0].send(data_arr)


if __name__ == '__main__':
    def main():
        myServer = Server()
        myServer.startServer()


    main()
