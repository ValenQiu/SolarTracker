# !/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from tkMessageBox import *
import time
import hashlib
import Adafruit_PCA9685
import os

LOG_LINE_NUM = 0

pwm = Adafruit_PCA9685.PCA9685()

pwm.set_pwm_freq(50)
servo_min = 150
servo_max = 600


def set_servo_pulse(channel, pulse):
    pulse_length = 1000000
    pulese_length //= 60
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096
    print('{0}us per bit'.format(pulse_length))
    pulse *= 100
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)


def set_servo_angle(channel, angle):
    angle = 4096 * ((angle * 12) + 500) / 20000
    pwm.set_pwm(channel, 0, int(angle))


class GUI():
    def __init__(self, window):
        self.window = window

    def set_window(self):
        # Set the window
        self.window.title("Solar Tracker")
        self.window.geometry('950x420+50+150')

        # Label
        self.speed_label = Label(self.window, text="Speed Adjustment")
        self.speed_label.grid(row=2, column=1)

        # self.break_label = Label(self.window, text="Break Time:")
        # self.break_label.grid(row=2, column=0)

        self.scan_label = Label(self.window, text="Scan Time:")
        self.scan_label.grid(row=3, column=0)

        self.azimuth_interval_label = Label(self.window, text="Azimuth Interval:")
        self.azimuth_interval_label.grid(row=4, column=0)

        self.zenith_interval_label = Label(self.window, text="Zenith Interval:")
        self.zenith_interval_label.grid(row=5, column=0)

        self.angle_label = Label(self.window, text="Angle")
        self.angle_label.grid(row=7, column=1)

        self.azimuth_label = Label(self.window, text="Azimuth:")
        self.azimuth_label.grid(row=8, column=0)

        self.zenith_label = Label(self.window, text="Zenith:")
        self.zenith_label.grid(row=10, column=0)

        self.log_label = Label(self.window, text="Log")
        self.log_label.grid(row=6, column=5)

        # Entry
        # self.break_time = Entry(self.window, font=('Arial', 14))
        # self.break_time.grid(row=2, column=1)

        self.sca = StringVar()
        self.scan_time = Entry(self.window, font=('Arial', 14), textvariable=self.sca)
        self.scan_time.grid(row=3, column=1)

        self.azi_int = StringVar()
        self.azimuth_interval = Entry(self.window, font=('Arial', 14),
                                      textvariable=self.azi_int)
        self.azimuth_interval.grid(row=4, column=1)

        self.zen_int = StringVar()
        self.zenith_interval = Entry(self.window, font=('Arial', 14),
                                     textvariable=self.zen_int)
        self.zenith_interval.grid(row=5, column=1)

        self.azi = StringVar()
        self.azimuth = Entry(self.window, font=('Arial', 14), textvariable=self.azi)
        self.azimuth.grid(row=8, column=1)

        self.zen = StringVar()
        self.zenith = Entry(self.window, font=('Arial', 14), textvariable=self.zen)
        self.zenith.grid(row=10, column=1)

        # log
        self.log_Text = Text(self.window, width=80, height=7, font=('Arial', 10))
        self.log_Text.grid(row=7, column=2, rowspan=5, columnspan=9)

        # Button
        self.scan_ip_button = Button(self.window, text="SCAN IP ADDRESS", bg="lightblue", width=30, height=2,
                                     command=self.str_scan_ip)
        self.scan_ip_button.grid(row=1, column=0, rowspan=1, columnspan=2)

        self.scan_button = Button(self.window, text="SCAN", bg="lightblue", width=15, height=2, command=self.scan)
        self.scan_button.grid(row=2, column=3)

        self.manual_button = Button(self.window, text="MANUAL", bg="lightblue", width=15, height=2, command=self.manual)
        self.manual_button.grid(row=4, column=3)

        self.custom_button = Button(self.window, text="CUSTOM", bg="lightblue", width=15, height=2, command=self.custom)
        self.custom_button.grid(row=2, column=5)

        self.reset_button = Button(self.window, text="RESET", bg="lightblue", width=15, height=2, command=self.reset)
        self.reset_button.grid(row=4, column=5)

        self.front_button = Button(self.window, text="FRONT", bg="lightblue", width=5, height=2,
                                   state=DISABLED, command=self.front)
        self.front_button.grid(row=3, column=8)

        self.back_button = Button(self.window, text="BACK", bg="lightblue", width=5, height=2,
                                  state=DISABLED, command=self.back)
        self.back_button.grid(row=5, column=8)

        self.left_button = Button(self.window, text="LEFT", bg="lightblue", width=5, height=2,
                                  state=DISABLED, command=self.left)
        self.left_button.grid(row=4, column=7)

        self.right_button = Button(self.window, text="RIGHT", bg="lightblue", width=5, height=2,
                                   state=DISABLED, command=self.right)
        self.right_button.grid(row=4, column=9)

        # space between features
        col_count, row_count = self.window.grid_size()

        for col in xrange(col_count):
            self.window.grid_columnconfigure(col, minsize=20)

        for row in xrange(row_count):
            self.window.grid_rowconfigure(row, minsize=20)

    def str_scan_ip(self):
        self.write_log_to_Text("Please see the command window")
        self.window.after(50, self.scan_ip)

    def scan_ip(self):
        print("Deteccting the IP Address, please wait")
        print("-------------------------------------------------------")
        os.chdir('/home/pi/wifi_recon_tool')
        os.system('sudo python ip_scan.py')
        print("-------------------------------------------------------")

    def str_scan(self):
        # print ("start")
        self.root = Tk()
        self.root.title("SCAN")
        self.root.geometry('300x100+250+150')

        self.scan_label = Label(self.root, text='Scanning', font=('Arial', 14))
        self.scan_label.pack()

        self.scan_cancel_button = Button(self.root, text='STOP', bg="lightblue", width=5, height=2,
                                         command=self.scan_stop)
        self.scan_cancel_button.pack()

        self.cancel_id = None
        self.lower_angle = 0
        self.upper_angle = 0
        self.direction = 0

        self.init()

    def init(self):
        set_servo_angle(1, 0)
        print("initialization of the lower motor")
        self.root.after(5000)
        set_servo_angle(2, 45)
        print("initialization of the upper motor")
        self.root.after(5000)
        self.write_log_to_Text("Initialization, Azimuth: 0 Zenith: 90")
        self.upper()

    def upper(self):
        if self.sca.get() == '':
            j = 2
        elif int(self.sca.get()) > 0:
            j = int(self.sca.get())
        else:
            j = 2

        if self.upper_angle <= 90:
            i = self.upper_angle / 2
            set_servo_angle(2, i)
            # print self.upper_angle
            self.write_log_to_Text("Upper: " + str(self.upper_angle) + " " + "Lower: " + str(self.lower_angle))
            self.cancel_id = self.root.after(j * 1000, self.lower)

        else:
            self.write_log_to_Text("Finished")
            # print ("finish")

    def lower(self):
        if self.sca.get() == '':
            j = 2
        elif int(self.sca.get()) > 0:
            j = int(self.sca.get())
        else:
            j = 2

        if not self.azi_int.get() == '':
            if int(self.azi_int.get()) > 0 and int(self.azi_int.get()) <= 360:
                azi = int(self.azi_int.get())
            else:
                print("out of range")
                azi = 10
        else:
            azi = 10

        if not self.zen_int.get() == '':
            if int(self.zen_int.get()) > 0 and int(self.zen_int.get()) < 90:
                zen = int(self.zen_int.get())
            else:
                print("out of range")
                zen = 6
        else:
            zen = 6

        if self.direction == 0:
            if self.lower_angle < 360:
                self.lower_angle += azi
                self.write_log_to_Text("Upper: " + str(self.upper_angle) + " " + "Lower: " + str(self.lower_angle))
                i = self.lower_angle / 2
                set_servo_angle(1, i)
                # print self.cancel_id
                self.cancel_id = self.root.after(j * 1000, self.lower)
            elif self.lower_angle == 360:
                self.direction = 1
                i = self.lower_angle / 2
                set_servo_angle(1, i)
                self.upper_angle += zen
                self.upper()

        elif self.direction == 1:
            if self.lower_angle > 0:
                self.lower_angle -= azi
                i = self.lower_angle / 2
                set_servo_angle(1, i)
                # print self.cancel_id
                self.write_log_to_Text("Upper: " + str(self.upper_angle) + " " + "Lower: " + str(self.lower_angle))
                self.root.after(j * 1000, self.lower)
            elif self.lower_angle == 0:
                self.direction = 0
                self.upper_angle += zen
                self.upper()

    def scan_stop(self):
        # print ("stop")
        if self.cancel_id is not None:
            self.root.after_cancel(self.cancel_id)
            self.cancel_id = None
            # print self.cancel_id
            self.write_log_to_Text("Canceled, other functions are available now")
            # print ("canceled")
        self.manual_button['state'] = NORMAL
        self.custom_button['state'] = NORMAL
        self.reset_button['state'] = NORMAL
        self.scan_button['state'] = NORMAL
        self.root.destroy()

    def scan(self):
        # print ("hi")
        self.write_log_to_Text("Start Scanning, other functions are forbidden now")
        self.scan_button['state'] = DISABLED
        self.manual_button['state'] = DISABLED
        self.custom_button['state'] = DISABLED
        self.reset_button['state'] = DISABLED
        res = askokcancel(message='Do you want to start scanning?')
        if res:
            self.str_scan()
        elif not res:
            # print ("goodbye")
            self.write_log_to_Text("Canceled, other functions are available now")
            self.manual_button['state'] = NORMAL
            self.custom_button['state'] = NORMAL
            self.reset_button['state'] = NORMAL
            self.scan_button['state'] = NORMAL
            pass

    def manual_lower_ini(self):
        set_servo_angle(1, self.pan / 2)
        # print ("Lower motor: Initialization")
        self.write_log_to_Text("Zenith: 90 Azimuth: 180")
        self.window.after(2000, self.manual_upper_ini)

    def manual_upper_ini(self):
        set_servo_angle(2, self.tilt / 2)
        # print ("Upper motor: Initialization")
        time.sleep(2)
        self.front_button['state'] = NORMAL
        self.back_button['state'] = NORMAL
        self.left_button['state'] = NORMAL
        self.right_button['state'] = NORMAL
        self.write_log_to_Text("Manual is available, other functions are forbidden now")
        # print ("Manual is able")

    def manual(self):
        if self.front_button['state'] == DISABLED:
            self.pan = 180  # pan for left/right
            self.tilt = 90  # tilt for front/back
            self.scan_button['state'] = DISABLED
            self.custom_button['state'] = DISABLED
            self.reset_button['state'] = DISABLED
            self.write_log_to_Text("Manual initialization")
            self.manual_lower_ini()
        else:
            self.front_button['state'] = DISABLED
            self.back_button['state'] = DISABLED
            self.left_button['state'] = DISABLED
            self.right_button['state'] = DISABLED
            self.scan_button['state'] = NORMAL
            self.custom_button['state'] = NORMAL
            self.reset_button['state'] = NORMAL
            print("Manual is disabled")

    def custom(self):
        self.window.after(2000, self.custom_lower)
        # print ("lower")
        self.write_log_to_Text("Custom")

    def custom_lower(self):
        # print type(self.azimuth.get())
        if self.azi.get() == "":
            # print ("no entry")
            self.write_log_to_Text("Azimuth no entry")
        elif int(self.azi.get()) >= 0 and int(self.azi.get()) <= 360:
            i = int(self.azi.get()) / 2
            set_servo_angle(1, i)
            print("upper")
            self.window.after(3000, self.custom_upper)
        else:
            print("out of range")

    def custom_upper(self):
        if self.zen.get() == "":
            # print ("no entry")
            self.write_log_to_Text("Zenith no entry")
        elif int(self.zen.get()) >= 30 and int(self.zen.get()) <= 90:
            i = int(self.zen.get())
            set_servo_angle(2, i / 2)
            self.write_log_to_Text("Upper: " + self.zen.get() + " " + "Lower: " + self.azi.get())
            print("done")
        else:
            print("out of range")

    def reset(self):
        # print ("reset")
        self.break_time.delete(0, END)
        self.scan_time.delete(0, END)
        self.azimuth_interval.delete(0, END)
        self.zenith_interval.delete(0, END)
        self.azimuth.delete(0, END)
        self.zenith.delete(0, END)
        self.write_log_to_Text("Reset")

    def left(self):
        # print ("left")
        self.pan += 2
        pan = self.pan
        if pan <= 360:
            set_servo_angle(1, pan / 2)
            self.write_log_to_Text("Zenith: " + str(self.tilt) + " " + "Azimuth: " + str(self.pan))
        else:
            self.pan -= 2
            # print "out of range"
            self.write_log_to_Text("Out of range")
            # print pan

    def right(self):
        # print ("right")
        self.pan -= 2
        pan = self.pan
        if pan >= 0:
            set_servo_angle(1, pan / 2)
            self.write_log_to_Text("Zenith: " + str(self.tilt) + " " + "Azimuth: " + str(self.pan))
        else:
            self.pan += 2
            self.write_log_to_Text("Out of range")
            # print "out of range"
            # print pan

    def front(self):
        # print ("front")
        self.tilt -= 2
        tilt = self.tilt
        if tilt >= 0:
            set_servo_angle(2, tilt / 2)
            self.write_log_to_Text("Zenith: " + str(self.tilt) + " " + "Azimuth: " + str(self.pan))
        else:
            self.tilt += 2
            self.write_log_to_Text("Out of range")
            # print "out of range"
            # print tilt

    def back(self):
        # print ("back")
        self.tilt += 2
        tilt = self.tilt
        if tilt <= 180:
            set_servo_angle(2, tilt / 2)
            self.write_log_to_Text("Zenith: " + str(self.tilt) + " " + "Azimuth: " + str(self.pan))
        else:
            self.tilt -= 2
            self.write_log_to_Text("Out of range")
            # print "out of range"
            # print tilt

    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return current_time

    # 日志动态打印
    def write_log_to_Text(self, logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + str(logmsg) + "\n"  # 换行
        # if LOG_LINE_NUM <= 7:
        self.log_Text.insert(END, logmsg_in)
        LOG_LINE_NUM = LOG_LINE_NUM + 1
        self.log_Text.yview_moveto(1)
        # else:
        # self.log_Text.delete(1.0,2.0)
        # self.log_Text.insert(END, logmsg_in)


def gui_start():
    window = Tk()
    ZMJ_PORTAL = GUI(window)
    ZMJ_PORTAL.set_window()
    window.mainloop()


gui_start()
