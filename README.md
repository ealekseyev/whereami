# Where Am I?
This project is a basic proof of concept that the relative position of a wifi device can be triangulated using the signal strengths of other devices, in this case WiFi routers, in the vicinity.

How it works:
An ESP32 is put into a perpetual scan mode. Once networks are scanned, the scan data is compressed and sent over USB to a computer running a python client. the client decodes the payload and logs it to a file, where the data is later lumped together and used to train a tensorflow model.
A separate python program runs the model, and while an ESP32 is hooked up the the host computer, will continually feed the WiFi signals into the TF network and output which room in the house the computer is currently in.
