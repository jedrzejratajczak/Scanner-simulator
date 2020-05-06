#!/usr/bin/env python3
import paho.mqtt.client as mqtt
from ClientPckg import Constants
from ClientPckg import Functions


class Terminal:
    terminal_id = Constants.TERMINAL_ID
    client = mqtt.Client()
    message_processed = False

    def __init__(self):
        self.client.tls_set(Constants.CRT_FILE_PATH)
        self.client.username_pw_set(Constants.USERNAME, Constants.PASSWORD)
        self.client.on_message = self.on_message_callback

    def connect_with_server(self):
        self.client.connect(Constants.BROKER, Constants.PORT)
        self.client.loop_start()
        self.client.subscribe(Constants.SUB_TOPIC)

    def disconnect_from_server(self):
        self.client.disconnect()

    def communicate_with_server(self, command):
        self.client.publish(Constants.PUB_TOPIC, command)
        self.message_processed = False
        while not self.message_processed:
            pass

    def on_message_callback(self, client, userdata, message):
        print(Functions.decode_message(message))
        self.message_processed = True
