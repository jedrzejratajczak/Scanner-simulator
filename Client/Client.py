import time
from subprocess import call


def secs_to_hours(secs):
    hours = 0
    mins = 0
    while secs >= 60:
        secs -= 60
        mins += 1
    while mins >= 60:
        mins -= 60
        hours += 1
    secs = int(secs)
    return str(hours) + ":" + str(mins) + "." + str(secs)

def write_to_info_file(content, file_name):
    info_file = open(file_name, "w")
    info_file.write(content)
    info_file.close()

def encrypt(content): #TODO zaszyfrowanie ciagu
    return content

class Terminal:
    __terminal_id = str
    __info_file_name = "info_file.txt"

    def __init__(self, terminal_id):
        self.__terminal_id = terminal_id

    def __communicate_with_server(self, command):
        #TODO potrzebne sprawdzanie czy serwer nie jest zajety
        write_to_info_file(command, self.__info_file_name)
        call('mosquitto_pub -h localhost -t "server/command" -f "info_file.txt"', shell=True)
        call('mosquitto_sub -h localhost -t "server/feedback" -N -C 1 > "info_file.txt"', shell=True)
        info_file = open(self.__info_file_name, "r")
        print(info_file.read())
        info_file.close()

    def __make_command(self, command, login, password, args=None):
        login = encrypt(login)
        password = encrypt(password)
        if args is not None:
            args_str = ""
            for i in range(len(args)):
                if i == len(args) - 1:
                    args_str += args[i]
                else:
                    args_str += args[i] + ','
            return command + ',' + self.__terminal_id + ',' + str(time.time()) + ',' + login + ',' + password + ',' + args_str
        else:
            return command + ',' + self.__terminal_id + ',' + str(time.time()) + ',' + login + ',' + password

    def shutdown(self, login, password):
        self.__communicate_with_server(self.__make_command("shutdown", login, password))

    def read_card(self, card_rfid, login, password):
        self.__communicate_with_server(self.__make_command("read_card", login, password, [card_rfid]))

    def add_terminal(self, terminal_id, login, password):
        self.__communicate_with_server(self.__make_command("add_terminal", login, password, [terminal_id]))

    def add_worker(self, worker_id, surname, name, login, password):
        self.__communicate_with_server(self.__make_command("add_worker", login, password, [worker_id, surname, name]))

    def assign(self, worker_id, card_rfid, login, password):
        self.__communicate_with_server(self.__make_command("assign", login, password, [worker_id, card_rfid]))

    def unassign(self, card_rfid, login, password):
        self.__communicate_with_server(self.__make_command("unassign", login, password, [card_rfid]))

    def delete_card(self, card_rfid, login, password):
        self.__communicate_with_server(self.__make_command("delete_card", login, password, [card_rfid]))

    def delete_terminal(self, terminal_id, login, password):
        self.__communicate_with_server(self.__make_command("delete_terminal", login, password, [terminal_id]))

    def delete_worker(self, worker_id, login, password):
        self.__communicate_with_server(self.__make_command("delete_worker", login, password, [worker_id]))

    def get_workers(self, login, password):
        self.__communicate_with_server(self.__make_command("get_workers", login, password))

    def get_cards(self, login, password):
        self.__communicate_with_server(self.__make_command("get_cards", login, password))

    def get_terminals(self, login, password):
        self.__communicate_with_server(self.__make_command("get_terminals", login, password))

def sign_in(): #TODO logowanie do sesji
    return "", ""

if __name__ == "__main__":
    session = ("", "")
    shutdown_flag = False
    terminal = Terminal("TER1")
    while not shutdown_flag:
        option_number = input("Choose an option number: ")
        if option_number == 0:
            shutdown_flag = True
            print("Goodbye")
        if option_number == 1:
            terminal.shutdown(session[0], session[1])
        if option_number == 2:
            card_rfid = raw_input('Type card rfid: ') #TODO zmiana z inputa na klawisz
            terminal.read_card(card_rfid, session[0], session[1])
        if option_number == 3:
            terminal_id = raw_input("Type terminal id: ")
            terminal.add_terminal(terminal_id, session[0], session[1])
        if option_number == 4:
            worker_id = raw_input("Type worker id: ")
            surname = raw_input("Type worker surname: ")
            name = raw_input("Type worker name: ")
            terminal.add_worker(worker_id, surname, name, session[0], session[1])
        if option_number == 5:
            worker_id = raw_input("Type worker id: ")
            card_rfid = raw_input("Type card rfid: ")
            terminal.assign(worker_id, card_rfid, session[0], session[1])
        if option_number == 6:
            card_rfid = raw_input("Type card rfid: ")
            terminal.unassign(card_rfid, session[0], session[1])
        if option_number == 7:
            card_rfid = raw_input("Type card rfid: ")
            terminal.delete_card(card_rfid, session[0], session[1])
        if option_number == 8:
            terminal_id = raw_input("Type terminal id: ")
            terminal.delete_terminal(terminal_id, session[0], session[1])
        if option_number == 9:
            worker_id = raw_input("Type worker id: ")
            terminal.delete_worker(worker_id, session[0], session[1])
        if option_number == 10:
            terminal.get_workers(session[0], session[1])
        if option_number == 11:
            terminal.get_cards(session[0], session[1])
        if option_number == 12:
            terminal.get_terminals(session[0], session[1])
        if option_number == 13:
            session = sign_in()
