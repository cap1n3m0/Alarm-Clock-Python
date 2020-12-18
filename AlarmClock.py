from tkinter import *
import datetime
import _thread
import time
import months as m
import times as t
import sys
from playsound import playsound

class Current: 
    hour = ""
    minute = ""
    second = ""

DATE = datetime.datetime

class Date:
    day = DATE.now().day
    month = DATE.now().month
    year = DATE.now().year

c = Current()
d = Date()

alarm = Tk()
alarm_on = False
stopwatch_on = False
time_up = False
target_hours = 0                  
time_rem = 0
temp = 0
mode = "alarm"
str_alarm_state = "Start Alarm"
str_stopwatch_state = "Start stopwatch"
show_current_time = True
header_text = ("Courier", 50)
title_font = ("Courier", 50)
time_font = ("Courier", 80)
alarm.config(bg = "#2B2B2B")
alarm.geometry("1600x1250")
t_set_alarm_for = Label(alarm, bg = "#2B2B2B", fg = "white", text = "Set alarm for", font = header_text)
l_alarm_time = Label(alarm, bg = "#2B2B2B", fg = "white") 
title = Label(alarm, text = "Alarm Clock and Timer", bg = "#2B2B2B", fg = "white", font = title_font)
title.place(relx = 0.197, rely = 0, relwidth = 0.6)



def show_date_time():  
    global c
    global d
    global time_font
    date_font = ("Courier", 20)
    l_stopwatch.place(relx = 0.3, rely = 0.45, relwidth = 0.4)
    t_date = Label(alarm, text = m.dates[str(d.month)] + " " + str(d.day) + ", " + str(d.year), font = date_font, bg = "#2B2B2B", fg = "white",)
    t_date.place(relx = 0.34, rely = 0.1, relwidth = 0.3)
    t_current_time = Label(alarm, font = time_font)
    t_current_time.place(relx = 0.2, rely = 0.25, relwidth = 0.6) 
    while show_current_time:
        if (DATE.now().hour < 10):
            c.hour = "0" + str(DATE.now().hour)
        else:
            c.hour = str(DATE.now().hour)
        if (DATE.now().minute < 10):
            c.minute = "0" + str(DATE.now().minute)
        else: 
            c.minute = str(DATE.now().minute)
        if (DATE.now().second < 10):
            c.second = "0" + str(DATE.now().second)
        else: 
            c.second = str(DATE.now().second)
        current_time = c.hour + ":" + c.minute + ":" + c.second
        t_current_time.config(bg = "#2B2B2B", fg = "white", text = current_time)
        time.sleep(1)


def update(*args):
    global target_hours
    global time_font
    l_alarm_time.config(text = str(target_hours) + " : " + def_minutes.get() + def_seconds.get() + " :  " + def_time_of_day.get(), bg = "#2B2B2B", fg = "white", font = time_font)
    if def_time_of_day.get() == "PM":
        if target_hours < 12: 
            target_hours = int(def_hours.get()) + 12
    elif target_hours == 12: 
        target_hours = 0    


# Show alarm clock 
def_hours = StringVar()
def_hours.set("00")
def_hours.trace("w", update)
def_minutes = StringVar()
def_minutes.set("00")
def_minutes.trace("w", update)
def_seconds = StringVar()
def_seconds.set("00")
def_seconds.trace("w", update)
def_time_of_day = StringVar()
def_time_of_day.set("AM")
def_time_of_day.trace("w", update)
drop_hours = OptionMenu(alarm, def_hours, *t.hours)
drop_minutes = OptionMenu(alarm, def_minutes, *t.minutes)
drop_seconds = OptionMenu(alarm, def_seconds, *t.seconds)
drop_time_of_day = OptionMenu(alarm, def_time_of_day, *t.time_of_day) 
l_stopwatch = Label(alarm, bg = "#2B2B2B", fg = "white", text = "Stopwatch time text")
elapsed_time = 0

def drop_forget(): 
    global drop_hours
    global drop_minutes
    global drop_seconds
    global drop_time_of_day
    drop_seconds.place_forget()
    drop_hours.place_forget()
    drop_minutes.place_forget()
    drop_time_of_day.place_forget()


def drop_place(): 
    global drop_hours
    global drop_minutes
    global drop_seconds
    global drop_time_of_day
    drop_hours.place(relx = 0.3, rely = 0.6, relwidth = 0.1)
    drop_minutes.place(relx = 0.4, rely = 0.6, relwidth = 0.1)
    drop_seconds.place(relx = 0.5, rely = 0.6, relwidth = 0.1)
    drop_time_of_day.place(relx = 0.6, rely = 0.6, relwidth = 0.1)
    drop_seconds.config(bg="#2B2B2B", fg = "white")
    drop_minutes.config(bg="#2B2B2B", fg = "white")
    drop_hours.config(bg="#2B2B2B", fg = "white")
    drop_time_of_day.config(bg="#2B2B2B", fg = "white")


def show_stopwatch():
    global l_stopwatch
    global drop_hours
    global drop_minutes
    global drop_seconds
    global drop_time_of_day
    global time_font
    global l_alarm_time
    l_stopwatch.config(text = "0:00:00", font = time_font, bg = "#2B2B2B", fg = "white",)
    l_stopwatch.place(relx = 0.3, rely = 0.45, relwidth = 0.4)
    drop_forget()
    l_alarm_time.place_forget()


def show_alarm_clock(): 
    global l_stopwatch
    global t_set_alarm_for
    global drop_hours
    global drop_minutes
    global drop_seconds
    global drop_time_of_day
    l_stopwatch.place_forget()
    t_set_alarm_for.place(relx = 0.20, rely = 0.45, relwidth = 0.6)
    drop_place()


def change_alarm_time():
    global alarm_on
    global c
    global time_rem
    global target_hours
    global def_minutes
    global def_seconds
    global time_up
    global drop_time_of_day
    global stopwatch_on
    if target_hours > 23: 
        target_hours = 12
    while not DATE(DATE.now().year, DATE.now().month, DATE.now().day, target_hours, int(def_minutes.get()), int(def_seconds.get())) == DATE(DATE.now().year, DATE.now().month, DATE.now().day, int(c.hour), int(c.minute), int(c.second)):
        future_time = DATE(DATE.now().year, DATE.now().month, DATE.now().day, target_hours, int(def_minutes.get()), int(def_seconds.get()))
        current_time = DATE(DATE.now().year, DATE.now().month, DATE.now().day, int(c.hour), int(c.minute), int(c.second))
        time_rem = future_time - current_time
        if not time_up: 
            if str(time_rem).find("-1 day,") == -1:
                l_alarm_time.config(text =  str(time_rem), font = time_font, bg = "#2B2B2B", fg = "white",)
            else:
                l_alarm_time.config(text =  str(time_rem).replace("-1 day,", " ", 1), font = time_font)
            time.sleep(1)
            if stopwatch_on or not alarm_on: 
                sys.exit()
        else: 
            l_alarm_time.config(text =  "Time Up!")
    if DATE(DATE.now().year, DATE.now().month, DATE.now().day, target_hours, int(def_minutes.get()), int(def_seconds.get())) - DATE(DATE.now().year, DATE.now().month, DATE.now().day, int(c.hour), int(c.minute), int(c.second)) == datetime.timedelta(seconds = 0): 
        time_up = True
        playsound('alarm.mp3')


def change_stopwatch_time(val): 
    global l_stopwatch
    global stopwatch_on
    global elapsed_time
    elapsed_time = val
    while stopwatch_on:
        if elapsed_time < 10: 
            l_stopwatch.config(text = "0:00:0" + str(elapsed_time))
        else: 
            l_stopwatch.config(text = "0:00:" + str(elapsed_time))
        elapsed_time += 1
        time.sleep(1)


def toggle_alarm_state(): 
    global alarm_on
    global stopwatch_on
    global time_up
    alarm_on = not alarm_on
    if alarm_on: 
        stopwatch_on = False
    if alarm_on and not stopwatch_on: 
        alarm_start_stop.config(text = "Stop Alarm")
        t_set_alarm_for.config(text = "Alarm running")
        drop_forget()
        l_alarm_time.place(relx = 0.17, rely = 0.55, relwidth = 0.6)
        time_up = False
        _thread.start_new_thread(change_alarm_time, ())
    if not alarm_on and not stopwatch_on: 
        alarm_start_stop.config(text =  "Start Alarm")
        t_set_alarm_for.config(text = "Set alarm for")
        drop_place()
        l_alarm_time.place_forget()
    if stopwatch_on and not alarm_on: 
        alarm_start_stop.place_forget()
        t_set_alarm_for.place_forget()
        drop_forget()
        l_alarm_time.place_forget()
        l_stopwatch.place(relx = 0.3, rely = 0.55, relwidth = 0.4)


def toggle_stopwatch_state(): 
    global stopwatch_on
    global alarm_start_stop
    global stopwatch_start_stop 
    global stopwatch_resume
    global alarm_on
    stopwatch_on = not stopwatch_on
    if stopwatch_on: 
        alarm_on = False
    alarm_start_stop.place_forget()
    if stopwatch_on and not alarm_on:
        stopwatch_resume.place_forget()
        stopwatch_start_stop.config(text = "Stop stopwatch")
        _thread.start_new_thread(change_stopwatch_time, (0, ))
    else:
        if elapsed_time > 0: 
           stopwatch_start_stop.config(text = "Restart stopwatch")
           stopwatch_resume.place(relx = 0.4, rely = 0.8, relwidth = 0.2)
        else: 
           stopwatch_start_stop.config(text = "Start stopwatch")
           stopwatch_resume.place(relx = 0.4, rely = 0.7, relwidth = 0.2)



def resume_stopwatch(elapsed_time, this): 
    global stopwatch_on 
    stopwatch_on = True
    stopwatch_start_stop.config(text = "Stop stopwatch")
    this.place_forget()
    _thread.start_new_thread(change_stopwatch_time, (elapsed_time, ))


stopwatch_start_stop = Button(alarm, highlightbackground = "#27b843", width = 30, height = 4, fg = "white", font = ("Courier", 16), text = str_stopwatch_state, command = toggle_stopwatch_state)
alarm_start_stop = Button(alarm, highlightbackground = "#27b843", width = 20, height = 4, fg = "white", font = ("Courier", 16), text = str_alarm_state, command = toggle_alarm_state)
stopwatch_resume = Button (
        alarm, highlightbackground = "#de4554", width = 30, height = 4, fg = "white", text = "Resume stopwatch", font = ("Courier", 16), 
        command = lambda: resume_stopwatch(elapsed_time, stopwatch_resume)
)


def to_switch(): 
    global mode
    global alarm_start_stop
    global stopwatch_start_stop
    if mode == "alarm": 
        alarm_start_stop.place(relx = 0.44, rely = 0.7, relwidth = 0.1)
        return show_alarm_clock()
    else: 
        stopwatch_start_stop.place(relx = 0.4, rely = 0.65, relwidth = 0.2)
        return show_stopwatch()


def switch_to_alarm():
    global mode
    global stopwatch_resume
    global stopwatch_start_stop
    global alarm_start_stop
    mode = "alarm"
    alarm_start_stop.place_forget()
    stopwatch_resume.place_forget()
    stopwatch_start_stop.place_forget()
    _thread.start_new_thread(to_switch, ())


def switch_to_stopwatch(): 
    global mode
    global resume_stopwatch
    global stopwatch_start_stop
    global alarm_start_stop
    mode = "stop"
    stopwatch_start_stop.place_forget()
    drop_forget()
    alarm_start_stop.place_forget()
    _thread.start_new_thread(to_switch, ())

radio_mode = StringVar()
radio_mode.set(mode)
stopwatch_b = Radiobutton(alarm,  bg = "#2B2B2B", fg = "white", font = ("Courier", 20), text =  "Stopwatch", height = 4, width = 10, variable = radio_mode, value = "stop", command = switch_to_stopwatch)
timer_b = Radiobutton(alarm,  bg = "#2B2B2B", fg = "white", font = ("Courier", 20), text = "Timer", height = 4, width = 10, variable = radio_mode, value = "alarm", command = switch_to_alarm)
stopwatch_b.place(relx = 0.54,rely = 0.9, relwidth = 0.2)
timer_b.place(relx = 0.3, rely = 0.9, relwidth = 0.2)
_thread.start_new_thread(show_date_time, ())
_thread.start_new_thread(to_switch, ())
alarm.mainloop()