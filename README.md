# Raspberry RFID Scanner Simulator with MQTT data transfer
A simple console simulation of raspberry pi's RFID cards scanner with MQTT data transfer feature.  
Program has been written in python and bash for Internet of Things course at Wroclaw University of Science and Technology.

**Author: Jędrzej Ratajczak**

## Table of content
* [General info](#general-info)
* [Screenshots](#screenshots)
* [Technologies](#technologies)
* [Setup](#setup)
* [Code Examples](#code-examples)
* [Features](#features)
* [Contact](#contact)

## General info
Program works on linux based systems (checked for Debian distro). Server and client has to be used on the same system as far.  
You will be notified with available commands after the program's execution. Defaultly there are 3 terminals,
10 new workers without work time and they are assigned to 10 cards.

## Screenshots
![Example screenshot](./img/screenshot.png)

## Technologies
* Python 3
* Mosquitto

## Setup
To execute client and server you will need to download *python* and *mosquitto* packages. Then enable mosquitto process.  
To start server you can use *python Server.py* command in *Server/* directory.  
To start client (terminal) you can use *python Client.py* command in *Client/* directory.

## Code examples
`2`  
`CARD2`  
\> Card read successfully  
`2`  
`CARD2`  
\> Your work time: 0:0.57

## Features
List of features ready:
* Read card (includes adding new card, changing worker state and printing worker's time)
* Delete or add terminal, card or worker
* Print list of terminals, cards or workers
* Assign or unassign card and reader
* Shutdown server remotely
* Shutdown terminal
* Writing and reading server backup on start and shutdown of server

To-do list:
* Signing in session of terminal
* Encryption and decryption of session information
* Permission to administrative functions for authenticated sessions

## Contact
Created by **Jędrzej Ratajczak** ([@mrozelek](https://github.com/Mrozelek)) - feel free to contact me!
