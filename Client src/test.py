import tensorflow as tf
import keras
from keras import layers
from database import *
from numpy import array as nparray
from esp_comms import *

num_wifi = 66
num_rooms = 7
rooms = ['kitchen', 'living room', 'master bedroom', 'Vera\'s room', 'Evan\'s room', 'hallway', 'garage', 'shared bathroom']
# Define Sequential model with 3 layers

mappings = Database.mapMacs('logdata_2268')
testEntries = Database.loadEntries('logdata2')
testI, testO = [], []
for entry in testEntries:
    i, o = Database.transformLogEntry(entry, mappings, (num_wifi, num_rooms))
    testI.append(i)
    testO.append(o)

model = tf.saved_model.load("logdata_2268.mdl")


esp = Comms('/dev/tty.usbserial-1410')
while True:
    frames = esp.readFrame()
    d = Database.framesToDict(frames)
    testI, _testO = Database.transformLogEntry(d, mappings, (num_wifi, num_rooms))

    outputs = model.serve(nparray([testI])).numpy().tolist()
    for i in range(len(outputs)):
        room = outputs[i].index(max(outputs[i]))+1
        percent = int(max(outputs[i])*100)
        print("Test sample " + str(i) + " results: " + str(percent) + "% likely to be the " + rooms[room-1])
