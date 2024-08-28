from tkinter import *
from tkinter.ttk import *
from GlobalVars import *
from time import sleep
from threading import Thread, Lock

cl_lock = Lock()
current_location = -1;

def _kitchen():
    global current_location, cl_lock, l1
    with cl_lock:
        current_location = 1
    l1.config(text="Kitchen")

def _livingroom():
    global current_location, l1
    cl_lock.acquire()
    current_location = 2
    cl_lock.release()
    l1.config(text="Living Room")


def _master():
    global current_location, l1
    cl_lock.acquire()
    current_location = 3
    cl_lock.release()
    l1.config(text="Master Bedroom")

def _vera():
    global current_location, l1
    cl_lock.acquire()
    current_location = 4
    cl_lock.release()
    l1.config(text="Vera's Room")

def _evan():
    global current_location, l1
    cl_lock.acquire()
    current_location = 5
    cl_lock.release()
    l1.config(text="Evan's Room")

def _hallway():
    global current_location, l1
    cl_lock.acquire()
    current_location = 6
    cl_lock.release()
    l1.config(text="Hallway")

def _garage():
    global current_location, l1
    cl_lock.acquire()
    current_location = 7
    cl_lock.release()
    l1.config(text="Garage")


def _bathroom1():
    global current_location, l1
    cl_lock.acquire()
    current_location = 8
    cl_lock.release()
    l1.config(text="Bathroom 1")

root = Tk()
root.geometry ('150x280')

b1 = Button(root, text = 'Kitchen', command = _kitchen)
b2 = Button(root, text = 'Living Room', command = _livingroom)
b3 = Button(root, text = 'Master Bedroom', command = _master)
b4 = Button(root, text = 'Vera\'s Room', command = _vera)
b5 = Button(root, text = 'Evan\'s Room', command = _evan)
b6 = Button(root, text = 'Hallway', command = _hallway)
b7 = Button(root, text = 'Garage', command = _garage)
b8 = Button(root, text = 'Bathroom 1', command = _bathroom1)
l1 = Label(root, text="Undefined Location")
          
b1.pack()
b2.pack()
b3.pack()
b4.pack()
b5.pack()
b6.pack()
b7.pack()
b8.pack()
l1.pack()