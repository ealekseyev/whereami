from threading import Thread, Lock
from tkinter import *
from tkinter.ttk import *
from time import sleep
from database import *
from esp_comms import Comms

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

def stringify(mac):
    return hex(mac[0])[2::] + ":" + hex(mac[1])[2::] + ":" + hex(mac[2])[2::] + ":" + hex(mac[3])[2::] + ":" + hex(mac[4])[2::] + ":" + hex(mac[5])[2::]

def training_run():
    global current_location, cl_lock
    logger = Logger("logdata_2268_2")
    esp = Comms('/dev/tty.usbserial-1410', baud=115200)

    # begin logging data
    while True:
        # if data collection is paused, or has not been initialized, then wait
        location = 0
        with cl_lock:
            location = current_location
        print(current_location)
        if location < 1:
            sleep(0.3)
            continue
        # else, log data:
        #print('reading')
        frames = esp.readFrame()
        #print('done reading')
        dict_frames = {}
        for frame in frames:
            dict_frames[stringify(frame)] = frame[6]
        print(dict_frames)
        with cl_lock:
            logger.write({current_location:dict_frames})
    
if __name__ == '__main__':
    # start the logging and gui threads
    ai_train = Thread(target=training_run)
    ai_train.start()
    root.mainloop()
