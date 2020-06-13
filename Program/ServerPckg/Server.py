#!/usr/bin/env python3
import paho.mqtt.client as mqtt
from ServerPckg.DatabasePckg.Database import Database
from ServerPckg import Constants


class Server:
    shutdown_flag = False
    database = Database()
    client = mqtt.Client()

    def __init__(self):
        self.database.load_state()
        self.client.tls_set(Constants.CRT_FILE_PATH)
        self.client.username_pw_set(Constants.USERNAME, Constants.PASSWORD)
        self.client.on_message = self.on_message_callback

    def connect(self):
        self.client.connect(Constants.BROKER, Constants.PORT)
        self.client.loop_start()
        self.client.subscribe(Constants.SUB_TOPIC)

    def on_message_callback(self, client, userdata, message):
        command_info = (str(message.payload.decode("utf-8"))).split(',')
        command_info[2] = float(command_info[2])
        if command_info[0] == Constants.SHUTDOWN_COMMAND:
            self.client.publish(Constants.PUB_TOPIC, self.database.shutdown(command_info[1], command_info[2]))
            self.client.loop_stop()
            self.client.disconnect()
            self.shutdown_flag = True
        if command_info[0] == Constants.READ_CARD_COMMAND:
            result = self.database.read_card(command_info[1], command_info[2], command_info[3])
            self.client.publish(Constants.PUB_TOPIC, result)
        if command_info[0] == Constants.ADD_TERMINAL_COMMAND:
            result = self.database.add_terminal(command_info[1], command_info[2], command_info[3])
            self.client.publish(Constants.PUB_TOPIC, result)
        if command_info[0] == Constants.ADD_WORKER_COMMAND:
            result = self.database.add_worker(command_info[1], command_info[2], command_info[3], command_info[4], command_info[5])
            self.client.publish(Constants.PUB_TOPIC, result)
        if command_info[0] == Constants.ASSIGN_COMMAND:
            result = self.database.assign(command_info[1], command_info[2], command_info[3], command_info[4])
            self.client.publish(Constants.PUB_TOPIC, result)
        if command_info[0] == Constants.UNASSIGN_COMMAND:
            result = self.database.unassign(command_info[1], command_info[2], command_info[3])
            self.client.publish(Constants.PUB_TOPIC, result)
        if command_info[0] == Constants.DELETE_CARD_COMMAND:
            result = self.database.delete_card(command_info[1], command_info[2], command_info[3])
            self.client.publish(Constants.PUB_TOPIC, result)
        if command_info[0] == Constants.DELETE_TERMINAL_COMMAND:
            result = self.database.delete_terminal(command_info[1], command_info[2], command_info[3])
            self.client.publish(Constants.PUB_TOPIC, result)
        if command_info[0] == Constants.DELETE_WORKER_COMMAND:
            result = self.database.delete_worker(command_info[1], command_info[2], command_info[3])
            self.client.publish(Constants.PUB_TOPIC, result)
        if command_info[0] == Constants.GET_WORKERS_COMMAND:
            result = self.database.get_workers(command_info[1], command_info[2])
            self.client.publish(Constants.PUB_TOPIC, result)
        if command_info[0] == Constants.GET_CARDS_COMMAND:
            result = self.database.get_cards(command_info[1], command_info[2])
            self.client.publish(Constants.PUB_TOPIC, result)
        if command_info[0] == Constants.GET_TERMINALS_COMMAND:
            result = self.database.get_terminals(command_info[1], command_info[2])
            self.client.publish(Constants.PUB_TOPIC, result)
