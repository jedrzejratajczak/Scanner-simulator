# Raspberry RFID Scanner Simulator with MQTT data transfer
A simple console simulation of raspberry pi's RFID cards scanner with MQTT data transfer feature.
Program has been written in python for Internet of Things course at Wroclaw University of Science and Technology.
In the 'screens with usage' folder you can check how the program works.

**Author: Jędrzej Ratajczak**

# How to use
Program works on linux based systems (checked for Debian distro). Server and client has to be used on the same system as far.

**To execute** client and server you will need to download *python* and *mosquitto* packages. Then enable mosquitto process.

**To start server** you can use *python Server.py* command in *Server/* directory.

**To start client** (terminal) you can use *python Client.py* command in *Client/* directory.

You will be notified with available commands after the program's execution. Defaultly there are 3 terminals,
10 new workers without work time and they are assigned to 10 cards.

# Repository's content
