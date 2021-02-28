# BATTLESHIP
Homework for Scientific Python course

## Purpose of the project
It is a well known game, it has 2 players and they are playing against each other. Both of them have a same size grid map and they have various sized ships. The main goal is to shoot torpedos to the other’s grid map, and sink all of the other player’s ships. In our project the game will have a basic GUI and it can be played either with a real player in multiplayer version on a server or either against an AI player on local.

## Table of contents

- [Gameplay](#gameplay)
- [User Interface](#user-interface)
- [Text UI](#text-ui)
- [GUI](#gui)
- [Requirements](#requirements)
- [Version control](#version-control)
- [Server-client connection](#server-client-connection)
- [Workflow](#workflow)
- [Things we need to learn in order to be able to do this project](#things-we-need-to-learn-in-order-to-be-able-to-do-this-project)


## Gameplay 
We create two 10 by 10 grids for the 2 players. 
In the initialization of the game both players can place their troops, namely:
- 1 pcs 1x5 ship
- 2 pcs 1x4 ship
- 3 pcs 1x3 ship
- 2 pcs 1x2 ship
- 2 pcs 1x1 ship

After that, players take turns guessing in their opponent's field (e.g. A1) and shoot a torpedo.
If their hint was correct, the ship (part) in that field will sink, if not, the torpedo will fall into the water. The player who sinks all of his opponent's ships wins.

## User Interface
We will create two interfaces, one for the console and another graphical. First the player has to decide if he/she wants to play a local or a network game. In case of network game, players choose a name and give the IP address where they want to connect. The server accepts the connections and responds. If the connection is successful, the player waits in a pool until his/her opponent arrives, then the game starts. The server does not accept connections until the end of the game. In the end of the game the server sends the results to the players.

## Text UI
First we develop our program with a Text UI. This UI has to show the current state of the game versus a robot created by us. Guesses of the player have to be written into the terminal and be sent by pressing ‘Enter’.

## GUI
In case of Graphical User Interface we show the current state (position of his/her ships, positions of previous hits and misses). 

## Requirements
The project has to use GUI interface networking and it has to include some machine player.
In case of networking the game is against a real player, in case of local game, the game is against the robot.

## Version control
There will be four main branches: master, gui, server, game logic.
The master branch will always have functional working code, and actual development will be on the other branches. If a task is finished in a branche it will be merged into the master branch.

## Server-client connection
The players and the server are going to be different python applications. The players will send their guesses (coordinates) to the server. 
The server will validate the guess and it’s going to calculate the new state and it will send this new state to the other player.
From the received new informations the player’s console or the GUI will refresh the game grid.

## Workflow
We start to develop the local game (with the machine player) in a Text UI. When this passes the tests, we focus on the network game still with Text UI. In the last part of the project we create the GUI suitable for local and network game too. 
We are using microsoft teams to assign tasks and track their progress.

## Things we need to learn in order to be able to do this project
- How do sockets work in python
- How can we create threads in python
- How our chosen GUI works
- How can we create a runnable .exe file from a bunch of .py files











