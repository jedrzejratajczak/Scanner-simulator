#!/usr/bin/env python3
import time


def make_command(command_name, terminal_id, args=None):
    if args is not None:
        args_str = ""
        for i in range(len(args)):
            if i == len(args) - 1:
                args_str += args[i]
            else:
                args_str += args[i] + ','
        return command_name + ',' + str(terminal_id) + ',' + str(time.time()) + ',' + args_str
    else:
        return command_name + ',' + str(terminal_id) + ',' + str(time.time())

def decode_message(message):
    return message.payload.decode("utf-8")
