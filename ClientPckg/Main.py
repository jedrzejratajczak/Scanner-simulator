#!/usr/bin/env python3
from ClientPckg.Terminal import Terminal
from ClientPckg import Functions
from ClientPckg import Constants


def disconnect(terminal : Terminal):
    terminal.client.disconnect()

def shutdown(terminal : Terminal):
    command = Functions.make_command(Constants.SHUTDOWN_COMMAND, terminal.terminal_id)
    terminal.communicate_with_server(command)

def read_card(terminal : Terminal, card_rfid):
    command = Functions.make_command(Constants.READ_CARD_COMMAND, terminal.terminal_id, [card_rfid])
    terminal.communicate_with_server(command)

def add_terminal(terminal : Terminal, terminal_id):
    command = Functions.make_command(Constants.ADD_TERMINAL_COMMAND, terminal.terminal_id, [terminal_id])
    terminal.communicate_with_server(command)

def add_worker(terminal : Terminal, worker_id, surname, name):
    command = Functions.make_command(Constants.ADD_WORKER_COMMAND, terminal.terminal_id, [worker_id, surname, name])
    terminal.communicate_with_server(command)

def assign(terminal : Terminal, worker_id, card_rfid):
    command = Functions.make_command(Constants.ASSIGN_COMMAND, terminal.terminal_id, [worker_id, card_rfid])
    terminal.communicate_with_server(command)

def unassign(terminal : Terminal, card_rfid):
    command = Functions.make_command(Constants.UNASSIGN_COMMAND, terminal.terminal_id, [card_rfid])
    terminal.communicate_with_server(command)

def delete_card(terminal : Terminal, card_rfid):
    command = Functions.make_command(Constants.DELETE_CARD_COMMAND, terminal.terminal_id, [card_rfid])
    terminal.communicate_with_server(command)

def delete_terminal(terminal : Terminal, terminal_id):
    command = Functions.make_command(Constants.DELETE_TERMINAL_COMMAND, terminal.terminal_id, [terminal_id])
    terminal.communicate_with_server(command)

def delete_worker(terminal : Terminal, worker_id):
    command = Functions.make_command(Constants.DELETE_WORKER_COMMAND, terminal.terminal_id, [worker_id])
    terminal.communicate_with_server(command)

def get_workers(terminal : Terminal):
    command = Functions.make_command(Constants.GET_WORKERS_COMMAND, terminal.terminal_id)
    terminal.communicate_with_server(command)

def get_cards(terminal : Terminal):
    command = Functions.make_command(Constants.GET_CARDS_COMMAND, terminal.terminal_id)
    terminal.communicate_with_server(command)

def get_terminals(terminal : Terminal):
    command = Functions.make_command(Constants.GET_TERMINALS_COMMAND, terminal.terminal_id)
    terminal.communicate_with_server(command)

if __name__ == "__main__":
    shutdown_flag = False
    terminal = Terminal()
    terminal.connect_with_server()
    while not shutdown_flag:
        option_number = input("Choose an option number (type 'help' for available commands): ")
        if option_number == 'help':
            print("Available commands:"
                  "\n0 - Close terminal"
                  "\n1 - Shutdown server"
                  "\n2 - Read card"
                  "\n3 - Add terminal"
                  "\n4 - Add worker"
                  "\n5 - Assign card to worker"
                  "\n6 - Unassign card"
                  "\n7 - Delete card"
                  "\n8 - Delete terminal"
                  "\n9 - Delete worker"
                  "\n10 - Get workers"
                  "\n11 - Get cards"
                  "\n12 - Get terminals")
        if option_number == '0':
            disconnect(terminal)
            shutdown_flag = True
            print("Goodbye")
        if option_number == '1':
            shutdown(terminal)
        if option_number == '2':
            card_rfid = input('Type card rfid: ')
            read_card(terminal, card_rfid)
        if option_number == '3':
            terminal_id = input("Type terminal id: ")
            add_terminal(terminal, terminal_id)
        if option_number == '4':
            worker_id = input("Type worker id: ")
            surname = input("Type worker surname: ")
            name = input("Type worker name: ")
            add_worker(terminal, worker_id, surname, name)
        if option_number == '5':
            worker_id = input("Type worker id: ")
            card_rfid = input("Type card rfid: ")
            assign(terminal, worker_id, card_rfid)
        if option_number == '6':
            card_rfid = input("Type card rfid: ")
            unassign(terminal, card_rfid)
        if option_number == '7':
            card_rfid = input("Type card rfid: ")
            delete_card(terminal, card_rfid)
        if option_number == '8':
            terminal_id = input("Type terminal id: ")
            delete_terminal(terminal, terminal_id)
        if option_number == '9':
            worker_id = input("Type worker id: ")
            delete_worker(terminal, worker_id)
        if option_number == '10':
            get_workers(terminal)
        if option_number == '11':
            get_cards(terminal)
        if option_number == '12':
            get_terminals(terminal)
