#!/usr/bin/env python3
import time


def secs_to_hours(secs):
    secs = int(secs)
    mins = 0
    hours = 0
    while secs >= 60:
        secs -= 60
        mins += 1
    while mins >= 60:
        mins -= 60
        hours += 1
    return str(hours) + ":" + str(mins) + "." + str(secs)

def secs_to_normal_time(secs):
    return str(time.localtime(secs)[2]) + "/" + str(time.localtime(secs)[1]) + "/" + str(
        time.localtime(secs)[0]) + " " + str(time.localtime(secs)[3]) + ":" + str(
        time.localtime(secs)[4]) + ":" + str(time.localtime(secs)[5])
