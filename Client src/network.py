import tensorflow as tf
import keras
from keras import layers
from database import *
from numpy import array as nparray

num_wifi = 66
num_rooms = 7
rooms = ['kitchen', 'living room', 'master bedroom', 'Vera\'s room', 'Evan\'s room', 'hallway', 'garage', 'shared bathroom']
# Define Sequential model with 3 layers

input_layer = keras.Input(shape=(num_wifi,))
hidden_layer = keras.layers.Dense(int((num_wifi+num_rooms)/2), activation="relu")(input_layer)
output_layer = keras.layers.Dense(num_rooms, activation="softmax")(hidden_layer)
model = keras.Model(inputs=input_layer, outputs=output_layer)


model.compile(optimizer='adam',
              loss='mse')

mappings = Database.mapMacs('logdata_2268')
entries = Database.loadEntries('logdata_2268')
inputs, outputs = [], []
for entry in entries:
    i, o = Database.transformLogEntry(entry, mappings, (num_wifi, num_rooms))
    inputs.append(i)
    outputs.append(o)

model.fit(x=nparray(inputs), y=nparray(outputs), epochs=200)

testEntries = Database.loadEntries('logdata2')
print(testEntries)
#while True: pass
testI, testO = [], []
for entry in testEntries:
    i, o = Database.transformLogEntry(entry, mappings, (num_wifi, num_rooms))
    testI.append(i)
    testO.append(o)
    
raw_out = model.predict(x=nparray(testI))
outputs = raw_out.tolist()
for i in range(len(outputs)):
    room = outputs[i].index(max(outputs[i]))+1
    percent = int(max(outputs[i])*100)
    print("Test sample " + str(i) + " results: " + str(percent) + "% likely to be the " + rooms[room-1])

s = input('Export? y/n: ')
if s == 'y':
    model.export('logdata_2268.mdl')
