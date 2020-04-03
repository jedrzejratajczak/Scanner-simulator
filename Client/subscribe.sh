#!/bin/bash
mosquitto_sub -h localhost -t "server/feedback" -C 1 > "info_file.txt"