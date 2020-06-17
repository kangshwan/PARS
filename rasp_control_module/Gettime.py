import time
import sys
#import RPI.GPIO as GPIO
import json

class File_control:
    def __init__(self, filename, wr_action, rd_action):
        self.fn_open = filename
        self.ac_wr = wr_action
        self.ac_rd = rd_action

    def openfile(self):
        f = open(self.fn_open, self.ac_wr)
        for i in range(0, 5):
            data = "%d users_setting_time:05:12:16:\n" %i   #05일 12시 16분
            f.write(data)
        f.close()
        return

    def readlines_obo(self):
        f = open(self.fn_open, self.ac_rd)
        lines = f.readlines()
        f.close()
        return lines

class Time_split:
    def __init__(self, timeline):
        self.timedata = timeline

    def split_time(self):
        Users_timeset = []
        Real_users_timeset = []
        for j in range(0, 4):
            b = self.timedata[j]
            Users_timeset = b.split(':')
            Real_users_timeset = Users_timeset[1:4]
        return Real_users_timeset

Open_files = File_control("babo.txt", "w", "r")
Open_files.openfile()
lines = Open_files.readlines_obo()

Split = Time_split(lines)
Split.split_time()


