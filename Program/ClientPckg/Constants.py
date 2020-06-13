#!/usr/bin/env python3
"""
MQTT CLIENT SETUP (note: all files should be in ServerPckg foler)
"""
PORT = 8883
BROKER = "PC"
CRT_FILE_PATH = "ca.crt"
SUB_TOPIC = "server/feedback"
PUB_TOPIC = "server/command"
USERNAME = 'client'
PASSWORD = 'password'

"""
OTHER
"""
TERMINAL_ID = "TER2"

"""
COMMAND NAMES
"""
SHUTDOWN_COMMAND = "shutdown"
READ_CARD_COMMAND = "read_card"
ADD_TERMINAL_COMMAND = "add_terminal"
ADD_WORKER_COMMAND = "add_worker"
ASSIGN_COMMAND = "assign"
UNASSIGN_COMMAND = "unassign"
DELETE_CARD_COMMAND = "delete_card"
DELETE_TERMINAL_COMMAND = "delete_terminal"
DELETE_WORKER_COMMAND = "delete_worker"
GET_WORKERS_COMMAND = "get_workers"
GET_CARDS_COMMAND = "get_cards"
GET_TERMINALS_COMMAND = "get_terminals"
