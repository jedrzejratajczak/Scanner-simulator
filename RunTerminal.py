from ClientPckg import Main

if __name__ == "__main__":
    shutdown_flag = False
    terminal = Main.Terminal()
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
            Main.disconnect(terminal)
            shutdown_flag = True
            print("Goodbye")
        if option_number == '1':
            Main.shutdown(terminal)
        if option_number == '2':
            card_rfid = input('Type card rfid: ')
            Main.read_card(terminal, card_rfid)
        if option_number == '3':
            terminal_id = input("Type terminal id: ")
            Main.add_terminal(terminal, terminal_id)
        if option_number == '4':
            worker_id = input("Type worker id: ")
            surname = input("Type worker surname: ")
            name = input("Type worker name: ")
            Main.add_worker(terminal, worker_id, surname, name)
        if option_number == '5':
            worker_id = input("Type worker id: ")
            card_rfid = input("Type card rfid: ")
            Main.assign(terminal, worker_id, card_rfid)
        if option_number == '6':
            card_rfid = input("Type card rfid: ")
            Main.unassign(terminal, card_rfid)
        if option_number == '7':
            card_rfid = input("Type card rfid: ")
            Main.delete_card(terminal, card_rfid)
        if option_number == '8':
            terminal_id = input("Type terminal id: ")
            Main.delete_terminal(terminal, terminal_id)
        if option_number == '9':
            worker_id = input("Type worker id: ")
            Main.delete_worker(terminal, worker_id)
        if option_number == '10':
            Main.get_workers(terminal)
        if option_number == '11':
            Main.get_cards(terminal)
        if option_number == '12':
            Main.get_terminals(terminal)
