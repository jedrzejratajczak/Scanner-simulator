#!/bin/bash
mosquitto_pub -h localhost -t "server/command" -f "info_file.txt"