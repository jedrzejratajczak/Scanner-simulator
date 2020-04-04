import time
from subprocess import call


class Card:
    worker_id = str
    rfid = str

    def __init__(self, rfid, worker_id = ""):
        self.rfid = rfid
        self.worker_id = worker_id


class Worker:
    worker_id = str
    surname = str
    name = str
    enter_time = float
    is_working = bool

    def __init__(self, worker_id, surname, name, enter_time=0., is_working=False):
        self.surname = surname
        self.name = name
        self.worker_id = worker_id
        self.enter_time = enter_time
        self.is_working = is_working


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

def secs_to_normal_time(secs):
    return str(time.localtime(secs)[2]) + "/" + str(time.localtime(secs)[1]) + "/" + str(
        time.localtime(secs)[0]) + " " + str(time.localtime(secs)[3]) + ":" + str(
        time.localtime(secs)[4]) + ":" + str(time.localtime(secs)[5])

def write_to_file(content, file_name):
    info_file = open(file_name, "w")
    info_file.write(content)
    info_file.close()

def decrypt(content): #TODO odszyfrowanie ciagu
    return content

class Server:
    shutdown_flag = False
    __workers_work_time = {}
    __terminals = []
    __workers = []
    __cards = []
    __logs = open("logs.txt", "a+")
    __info_file_name = "info_file.txt"

    def communicate_with_client(self):
        call('mosquitto_sub -h localhost -t "server/command" -N -C 1 > "info_file.txt"', shell=True)
        info_file = open(self.__info_file_name, "r")
        command = info_file.read()
        info_file.close()
        write_to_file(self.__command_handler(command), self.__info_file_name)
        time.sleep(0.1)
        call('mosquitto_pub -h localhost -t "server/feedback" -f "info_file.txt"', shell=True)

    def __command_handler(self, command):
        command_info = command.split(',')
        command_info[2] = float(command_info[2])
        if command_info[0] == "shutdown":
            return self.__shutdown(command_info[1], command_info[2], command_info[3], command_info[4])
        if command_info[0] == "read_card":
            return self.__read_card(command_info[1], command_info[2], command_info[3], command_info[4], command_info[5])
        if command_info[0] == "add_terminal":
            return self.__add_terminal(command_info[1], command_info[2], command_info[3], command_info[4], command_info[5])
        if command_info[0] == "add_worker":
            return self.__add_worker(command_info[1], command_info[2], command_info[3], command_info[4], command_info[5], command_info[6], command_info[7])
        if command_info[0] == "assign":
            return self.__assign(command_info[1], command_info[2], command_info[3], command_info[4], command_info[5], command_info[6])
        if command_info[0] == "unassign":
            return self.__unassign(command_info[1], command_info[2], command_info[3], command_info[4], command_info[5])
        if command_info[0] == "delete_card":
            return self.__delete_card(command_info[1], command_info[2], command_info[3], command_info[4], command_info[5])
        if command_info[0] == "delete_terminal":
            return self.__delete_terminal(command_info[1], command_info[2], command_info[3], command_info[4], command_info[5])
        if command_info[0] == "delete_worker":
            return self.__delete_worker(command_info[1], command_info[2], command_info[3], command_info[4], command_info[5])
        if command_info[0] == "get_workers":
            return self.__get_workers(command_info[1], command_info[2], command_info[3], command_info[4])
        if command_info[0] == "get_cards":
            return self.__get_cards(command_info[1], command_info[2], command_info[3], command_info[4])
        if command_info[0] == "get_terminals":
            return self.__get_terminals(command_info[1], command_info[2], command_info[3], command_info[4])
        self.__logs.write("invalid_command," + command_info[0])
        return "Invalid command"

    def __write_log(self, command, terminal_id, use_time, args=None):
        if args is not None:
            args_str = ""
            for i in range(len(args)):
                if i == len(args) - 1:
                    args_str += args[i]
                else:
                    args_str += args[i] + ','
            self.__logs.write(command + ',' + terminal_id + ',' + secs_to_normal_time(use_time) + ',' + args_str + '\n')
        else:
            self.__logs.write(command + ',' + terminal_id + ',' + secs_to_normal_time(use_time) + '\n')

    def __check_authorization(self, terminal_id, use_time):
        if not self.__authorise_terminal(terminal_id):
            self.__write_log("unauthorised", terminal_id, use_time)
            return False
        return True

    def __check_session(self, login, password): #TODO sprawdzenie loginu i hasla
        decrypt(login)
        decrypt(password)
        return True

    def __shutdown(self, terminal_id, use_time, login, password):
        if not self.__check_authorization(terminal_id, use_time):
            return "Unauthorised terminal"
        if not self.__check_session(login, password):
            return "Unauthorised session"
        self.shutdown_flag = True
        self.__write_log("shutdown", terminal_id, use_time)
        return "Server will shutdown"

    def __read_card(self, terminal_id, use_time, login, password, card_rfid):
        if not self.__check_authorization(terminal_id, use_time):
            return "Unauthorised terminal"
        card = self.__get_card(card_rfid)
        if card is None:
            if not self.__check_session(login, password):
                return "Unauthorised session"
            self.__cards.append(Card(card_rfid))
            self.__write_log("add_card", terminal_id, use_time, [card_rfid])
            return "Card added successfully"
        worker = self.__get_worker(card.worker_id)
        if worker is None:
            self.__write_log("read_card_fail", terminal_id, use_time, [card_rfid])
            return "No worker assigned to the card"
        if worker.is_working:
            worker.is_working = False
            self.__write_log("leave", terminal_id, use_time, [card_rfid, worker.worker_id])
            return self.__count_worker_time(terminal_id, use_time, worker)
        else:
            worker.is_working = True
            worker.enter_time = use_time
            self.__write_log("enter", terminal_id, use_time, [card_rfid, worker.worker_id])
            return "Card read successfull"

    def __add_terminal(self, terminal_id, use_time, login, password, add_terminal_id):
        if not self.__check_authorization(terminal_id, use_time):
            return "Unauthorised terminal"
        if not self.__check_session(login, password):
            return "Unauthorised session"
        if self.__authorise_terminal(add_terminal_id) is True:
            self.__write_log("add_terminal_fail", terminal_id, use_time, [add_terminal_id])
            return "Terminal already in database"
        self.__terminals.append(add_terminal_id)
        self.__write_log("add_terminal", terminal_id, use_time, [add_terminal_id])
        return "Terminal added successfully"

    def __add_worker(self, terminal_id, use_time, login, password, worker_id, surname, name):
        if not self.__check_authorization(terminal_id, use_time):
            return "Unauthorised terminal"
        if not self.__check_session(login, password):
            return "Unauthorised session"
        if self.__get_worker(worker_id) is not None:
            self.__write_log("add_worker_fail", terminal_id, use_time, [worker_id, surname, name])
            return "Worker already in database"
        self.__workers.append(Worker(worker_id, surname, name))
        self.__workers_work_time[worker_id] = 0.
        self.__write_log("add_worker", terminal_id, use_time, [worker_id, surname, name])
        return "Worker added successfully"

    def __assign(self, terminal_id, use_time, login, password, card_rfid, worker_id):
        if not self.__check_authorization(terminal_id, use_time):
            return "Unauthorised terminal"
        if not self.__check_session(login, password):
            return "Unauthorised session"
        card = self.__get_card(card_rfid)
        if card is None:
            self.__write_log("assign_fail", terminal_id, use_time, [card_rfid, worker_id])
            return "No such card in database"
        worker = self.__get_worker(worker_id)
        if worker is None:
            self.__write_log("assign_fail", terminal_id, use_time, [card_rfid, worker_id])
            return "No such worker hired"
        card.worker_id = worker_id
        self.__write_log("assign", terminal_id, use_time, [card_rfid, worker_id])
        return "Card assigned to worker successfully"

    def __unassign(self, terminal_id, use_time, login, password, card_rfid):
        if not self.__check_authorization(terminal_id, use_time):
            return "Unauthorised terminal"
        if not self.__check_session(login, password):
            return "Unauthorised session"
        card = self.__get_card(card_rfid)
        if card is None:
            self.__write_log("unassign_fail", terminal_id, use_time, [card_rfid])
            return "No such card in database"
        self.__write_log("unassign", terminal_id, use_time, [card_rfid, card.worker_id])
        card.worker_id = ""
        return "Card unassigned successfully"

    def __delete_card(self, terminal_id, use_time, login, password, card_rfid):
        if not self.__check_authorization(terminal_id, use_time):
            return "Unauthorised terminal"
        if not self.__check_session(login, password):
            return "Unauthorised session"
        card = self.__get_card(card_rfid)
        if card is None:
            self.__write_log("delete_card_fail", terminal_id, use_time, [card_rfid])
            return "No such card in database"
        self.__cards.remove(card)
        self.__write_log("delete_card", terminal_id, use_time, [card_rfid])
        return "Card successfully deleted"

    def __delete_terminal(self, terminal_id, use_time, login, password, delete_terminal_id):
        if not self.__check_authorization(terminal_id, use_time):
            return "Unauthorised terminal"
        if not self.__check_session(login, password):
            return "Unauthorised session"
        if not self.__authorise_terminal(delete_terminal_id):
            self.__write_log("delete_terminal_fail", terminal_id, use_time, [delete_terminal_id])
            return "No such terminal in database"
        self.__terminals.remove(delete_terminal_id)
        self.__write_log("delete_terminal", terminal_id, use_time, [delete_terminal_id])
        return "Terminal deleted successfully"

    def __delete_worker(self, terminal_id, use_time, login, password, worker_id):
        if not self.__check_authorization(terminal_id, use_time):
            return "Unauthorised terminal"
        if not self.__check_session(login, password):
            return "Unauthorised session"
        worker = self.__get_worker(worker_id)
        if worker is None:
            self.__write_log("delete_worker_fail", terminal_id, use_time, [worker_id])
            return "No such worker hired"
        self.__workers.remove(worker)
        self.__write_log("delete_worker", terminal_id, use_time, [worker_id])
        return "Worker fired successfully"

    def __get_workers(self, terminal_id, use_time, login, password):
        if not self.__check_authorization(terminal_id, use_time):
            return "Unauthorised terminal"
        if not self.__check_session(login, password):
            return "Unauthorised session"
        result = ""
        for worker in self.__workers:
            result += worker.worker_id + ',' + worker.surname + ',' + worker.name + '\n'
        self.__write_log("get_workers", terminal_id, use_time)
        return result

    def __get_cards(self, terminal_id, use_time, login, password):
        if not self.__check_authorization(terminal_id, use_time):
            return "Unauthorised terminal"
        if not self.__check_session(login, password):
            return "Unauthorised session"
        result = ""
        for card in self.__cards:
            result += card.rfid + ',' + card.worker_id + '\n'
        self.__write_log("get_cards", terminal_id, use_time)
        return result

    def __get_terminals(self, terminal_id, use_time, login, password):
        if not self.__check_authorization(terminal_id, use_time):
            return "Unauthorised terminal"
        if not self.__check_session(login, password):
            return "Unauthorised session"
        result = ""
        for terminal in self.__terminals:
            result += terminal + '\n'
        self.__write_log("get_terminals", terminal_id, use_time)
        return result

    def __count_worker_time(self, terminal_id, use_time, worker):
        self.__workers_work_time[worker.worker_id] += (use_time - worker.enter_time)
        self.__write_log("count_worker_time", terminal_id, use_time, [worker.worker_id])
        return "Your work time: " + secs_to_hours(self.__workers_work_time[worker.worker_id])

    def __get_worker(self, worker_id):
        for worker in self.__workers:
            if worker.worker_id == worker_id:
                return worker
        return None

    def __get_card(self, card_rfid):
        for card in self.__cards:
            if card.rfid == card_rfid:
                return card
        return None

    def __authorise_terminal(self, terminal_id):
        for i in range(len(self.__terminals)):
            if self.__terminals[i] == terminal_id:
                return True
        return False

    def save_state(self):
        file = open("workers.txt", "w")
        for worker in self.__workers:
            file.write(worker.worker_id + ',' + worker.surname + ',' + worker.name + ',' + str(worker.enter_time) + ',' + str(worker.is_working) + '\n')
        file.close()
        file = open("work_times.txt", "w")
        work_times = self.__workers_work_time.items()
        for work_time in work_times:
            file.write(str(work_time[0]) + ',' + str(work_time[1]) + '\n')
        file.close()
        file = open("terminals.txt", "w")
        for terminal_id in self.__terminals:
            file.write(str(terminal_id + '\n'))
        file.close()
        file = open("cards.txt", "w")
        for card in self.__cards:
            file.write(card.rfid + ',' + card.worker_id + '\n')
        file.close()

    def load_state(self):
        file = open("workers.txt", "r")
        workers_content = file.read().splitlines()
        for worker in workers_content:
            worker_info = worker.split(',')
            if worker_info[4] == "False":
                worker_is_working = False
            else:
                worker_is_working = True
            self.__workers.append(Worker(worker_info[0], worker_info[1], worker_info[2], float(worker_info[3]), worker_is_working))
        file.close()

        file = open("terminals.txt", "r")
        for terminal_id in file.read().splitlines():
            self.__terminals.append(terminal_id)
        file.close()

        file = open("cards.txt", "r")
        for card in file.read().splitlines():
            card_info = card.split(',')
            self.__cards.append(Card(card_info[0], card_info[1]))
        file.close()

        file = open("work_times.txt", "r")
        for work_time in file.read().splitlines():
            work_time_info = work_time.split(',')
            self.__workers_work_time[work_time_info[0]] = work_time_info[1]
        file.close()

if __name__ == "__main__":
    server = Server()
    server.load_state()
    while not server.shutdown_flag:
        server.communicate_with_client()
    server.save_state()
