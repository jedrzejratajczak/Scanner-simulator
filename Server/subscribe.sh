#!/bin/bash
mosquitto_sub -h localhost -t "server/command" -C 1 > "info_file.txt"