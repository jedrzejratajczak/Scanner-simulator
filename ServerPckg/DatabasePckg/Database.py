#!/usr/bin/env python3
from ServerPckg import Functions
from ServerPckg import Constants


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


class Database:
    workers_work_time = {}
    terminals = []
    workers = []
    cards = []
    logs = open(Constants.LOGS_FILE_PATH, "a+")

    def __write_log(self, command, terminal_id, use_time, args=None):
        if args is not None:
            args_str = ""
            for i in range(len(args)):
                if i == len(args) - 1:
                    args_str += args[i]
                else:
                    args_str += args[i] + ','
            self.logs.write(command + ',' + terminal_id + ',' + Functions.secs_to_normal_time(use_time) + ',' + args_str + '\n')
        else:
            self.logs.write(command + ',' + terminal_id + ',' + Functions.secs_to_normal_time(use_time) + '\n')

    def __check_authorization(self, terminal_id, use_time):
        if not self.__authorise_terminal(terminal_id):
            self.__write_log("unauthorised", terminal_id, use_time)
            return False
        return True

    def shutdown(self, terminal_id, use_time):
        if not self.__check_authorization(terminal_id, use_time):
            return "Unauthorised terminal"
        self.__write_log("shutdown", terminal_id, use_time)
        self.__save_state()
        return "Server will shutdown"

    def read_card(self, terminal_id, use_time, card_rfid):
        if not self.__check_authorization(terminal_id, use_time):
            return "Unauthorised terminal"
        card = self.__get_card(card_rfid)
        if card is None:
            self.cards.append(Card(card_rfid))
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

    def add_terminal(self, terminal_id, use_time, add_terminal_id):
        if not self.__check_authorization(terminal_id, use_time):
            return "Unauthorised terminal"
        if self.__authorise_terminal(add_terminal_id) is True:
            self.__write_log("add_terminal_fail", terminal_id, use_time, [add_terminal_id])
            return "Terminal already in database"
        self.terminals.append(add_terminal_id)
        self.__write_log("add_terminal", terminal_id, use_time, [add_terminal_id])
        return "Terminal added successfully"

    def add_worker(self, terminal_id, use_time, worker_id, surname, name):
        if not self.__check_authorization(terminal_id, use_time):
            return "Unauthorised terminal"
        if self.__get_worker(worker_id) is not None:
            self.__write_log("add_worker_fail", terminal_id, use_time, [worker_id, surname, name])
            return "Worker already in database"
        self.workers.append(Worker(worker_id, surname, name))
        self.workers_work_time[worker_id] = 0.
        self.__write_log("add_worker", terminal_id, use_time, [worker_id, surname, name])
        return "Worker added successfully"

    def assign(self, terminal_id, use_time, worker_id, card_rfid):
        if not self.__check_authorization(terminal_id, use_time):
            return "Unauthorised terminal"
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

    def unassign(self, terminal_id, use_time, card_rfid):
        if not self.__check_authorization(terminal_id, use_time):
            return "Unauthorised terminal"
        card = self.__get_card(card_rfid)
        if card is None:
            self.__write_log("unassign_fail", terminal_id, use_time, [card_rfid])
            return "No such card in database"
        self.__write_log("unassign", terminal_id, use_time, [card_rfid, card.worker_id])
        card.worker_id = ""
        return "Card unassigned successfully"

    def delete_card(self, terminal_id, use_time, card_rfid):
        if not self.__check_authorization(terminal_id, use_time):
            return "Unauthorised terminal"
        card = self.__get_card(card_rfid)
        if card is None:
            self.__write_log("delete_card_fail", terminal_id, use_time, [card_rfid])
            return "No such card in database"
        self.cards.remove(card)
        self.__write_log("delete_card", terminal_id, use_time, [card_rfid])
        return "Card successfully deleted"

    def delete_terminal(self, terminal_id, use_time, delete_terminal_id):
        if not self.__check_authorization(terminal_id, use_time):
            return "Unauthorised terminal"
        if not self.__authorise_terminal(delete_terminal_id):
            self.__write_log("delete_terminal_fail", terminal_id, use_time, [delete_terminal_id])
            return "No such terminal in database"
        self.terminals.remove(delete_terminal_id)
        self.__write_log("delete_terminal", terminal_id, use_time, [delete_terminal_id])
        return "Terminal deleted successfully"

    def delete_worker(self, terminal_id, use_time, worker_id):
        if not self.__check_authorization(terminal_id, use_time):
            return "Unauthorised terminal"
        worker = self.__get_worker(worker_id)
        if worker is None:
            self.__write_log("delete_worker_fail", terminal_id, use_time, [worker_id])
            return "No such worker hired"
        self.workers.remove(worker)
        self.__write_log("delete_worker", terminal_id, use_time, [worker_id])
        return "Worker fired successfully"

    def get_workers(self, terminal_id, use_time):
        if not self.__check_authorization(terminal_id, use_time):
            return "Unauthorised terminal"
        result = ""
        for worker in self.workers:
            result += worker.worker_id + ',' + worker.surname + ',' + worker.name + '\n'
        self.__write_log("get_workers", terminal_id, use_time)
        return result

    def get_cards(self, terminal_id, use_time):
        if not self.__check_authorization(terminal_id, use_time):
            return "Unauthorised terminal"
        result = ""
        for card in self.cards:
            result += card.rfid + ',' + card.worker_id + '\n'
        self.__write_log("get_cards", terminal_id, use_time)
        return result

    def get_terminals(self, terminal_id, use_time):
        if not self.__check_authorization(terminal_id, use_time):
            return "Unauthorised terminal"
        result = ""
        for terminal in self.terminals:
            result += terminal + '\n'
        self.__write_log("get_terminals", terminal_id, use_time)
        return result

    def __count_worker_time(self, terminal_id, use_time, worker):
        self.workers_work_time[worker.worker_id] += (use_time - worker.enter_time)
        self.__write_log("count_worker_time", terminal_id, use_time, [worker.worker_id])
        return "Your work time: " + Functions.secs_to_hours(self.workers_work_time[worker.worker_id])

    def __get_worker(self, worker_id):
        for worker in self.workers:
            if worker.worker_id == worker_id:
                return worker
        return None

    def __get_card(self, card_rfid):
        for card in self.cards:
            if card.rfid == card_rfid:
                return card
        return None

    def __authorise_terminal(self, terminal_id):
        for i in range(len(self.terminals)):
            if self.terminals[i] == terminal_id:
                return True
        return False

    def __save_state(self):
        file = open(Constants.WORKERS_FILE_PATH, "w")
        for worker in self.workers:
            file.write(worker.worker_id + ',' + worker.surname + ',' + worker.name + ',' + str(worker.enter_time) + ',' + str(worker.is_working) + '\n')
        file.close()
        file = open(Constants.WORKTIMES_FILE_PATH, "w")
        work_times = self.workers_work_time.items()
        for work_time in work_times:
            file.write(str(work_time[0]) + ',' + str(work_time[1]) + '\n')
        file.close()
        file = open(Constants.TERMINALS_FILE_PATH, "w")
        for terminal_id in self.terminals:
            file.write(str(terminal_id + '\n'))
        file.close()
        file = open(Constants.CARDS_FILE_PATH, "w")
        for card in self.cards:
            file.write(card.rfid + ',' + card.worker_id + '\n')
        file.close()

    def load_state(self):
        file = open(Constants.WORKERS_FILE_PATH, "r")
        workers_content = file.read().splitlines()
        for worker in workers_content:
            worker_info = worker.split(',')
            if worker_info[4] == "False":
                worker_is_working = False
            else:
                worker_is_working = True
            self.workers.append(Worker(worker_info[0], worker_info[1], worker_info[2], float(worker_info[3]), worker_is_working))
            self.workers_work_time[worker_info[0]] = 0
        file.close()

        file = open(Constants.TERMINALS_FILE_PATH, "r")
        for terminal_id in file.read().splitlines():
            self.terminals.append(terminal_id)
        file.close()

        file = open(Constants.CARDS_FILE_PATH, "r")
        for card in file.read().splitlines():
            card_info = card.split(',')
            self.cards.append(Card(card_info[0], card_info[1]))
        file.close()

        file = open(Constants.WORKTIMES_FILE_PATH, "r")
        for work_time in file.read().splitlines():
            work_time_info = work_time.split(',')
            self.workers_work_time[work_time_info[0]] = float(work_time_info[1])
        file.close()
