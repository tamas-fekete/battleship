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
        self.serversocket.bind((ip_address, 5001))
        # listen for connections
        self.serversocket.listen()
        # list of connections
        self.connection = []
        self.waitingForConnections()

        self.player1 = PlayerState(gui=None, randomShips=False)
        self.player2 = PlayerState(gui=None, randomShips=False)

    def waitingForConnections(self):

        while len(self.connection) < 2:
            conn, addr = self.serversocket.accept()
            self.connection.append(conn)
            print("player" + str(len(self.connection)) + "joined")
            # print(conn)
            # print(self.connection)

    def receiveFromPlayer1(self):
        return pickle.loads(self.connection[0].recv(1024))

    def receiveFromPlayer2(self):
        return pickle.loads(self.connection[1].recv(1024))

    def sendToPlayer1(self, data):
        data = pickle.dumps(data)
        self.connection[0].send(data)

    def sendToPlayer2(self, data):
        data = pickle.dumps(data)
        self.connection[1].send(data)

    def startServer(self):
        # main server loop
        guiShips1 = self.player1.initShips()
        self.sendToPlayer1(guiShips1)
        self.sendToPlayer1("Attacker")  # player 1 attacks first

        guiShips2 = self.player2.initShips()
        self.sendToPlayer2(guiShips2)
        self.sendToPlayer2("Defender")

        while True:
            print("waiting for player 1 attack coordinates")
            attackCoordinate = self.receiveFromPlayer1()
            print("received attack coordinates from player 1")
            response = self.player2.responseOfMissile(self.player1.shoot(attackCoordinate))
            self.player1.updateOpponentState(response)

            print("sending opponent state to player 1")
            self.sendToPlayer1(self.player1.opponentState)
            print("sending state to player 2")
            self.sendToPlayer2(self.player2.state)

            print("waiting for player 2 attack coordinates")
            attackCoordinate = self.receiveFromPlayer2()
            print("received attack coordinates from player 2")
            response = self.player1.responseOfMissile(self.player2.shoot(attackCoordinate))
            self.player2.updateOpponentState(response)

            print("sending opponent state to player 2")
            self.sendToPlayer2(self.player2.opponentState)
            print("sending state to player 1")
            self.sendToPlayer1(self.player1.state)


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


if __name__ == '__main__':
    def main():
        myServer = Server()
        myServer.startServer()


    main()
