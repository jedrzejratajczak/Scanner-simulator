#!/bin/bash
mosquitto_pub -h localhost -t "server/feedback" -f "info_file.txt"