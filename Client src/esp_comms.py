import serial
from time import sleep, time
class Comms:
    conn = None
    port = None
    def __init__(self, port, baud=115200):
        try:
            self.conn = serial.Serial(port, baud, timeout=4)
            self.port = port
            print('Connected!')
        except Exception as e:
            print(e)
            exit()
        pass

    def readFrame(self, recursion=0):
        #if(recursion>=2):
        #    self.__init__(self.port)
        self.conn.write(serial.to_bytes([1,1,1]))
        self.conn.flush()
        while(self.conn.in_waiting == 0):
            pass
        # wait for data to start transfer
        prev, cur = 1, 1
        while(prev != 0 or cur != 0):
            prev = cur
            #print('reading')
            cur = int.from_bytes(self.conn.read(1))
            #print('done reading')
        #self.conn.read(1)

        #print('continuing')
        prev, cur = 1, 1
        buf = []
        while(prev != 0 or cur != 0):
            prev = cur
            #print(self.conn.in_waiting)
            #t = time()
            while(self.conn.in_waiting < 1): pass
                #if(time() - t < 2):
                #    self.conn.flush()
                #    return self.readFrame(recursion=recursion+1)
            cur = int.from_bytes(self.conn.read(1))
            buf.append(cur)
        buf = buf[0:len(buf)-1]
        #print('returning')
        # 2d the array
        buf = [buf[i*7:i*7+7] for i in range(int(len(buf)/7))]
        return buf
    
if __name__ == '__main__':
    c = Comms('/dev/tty.usbserial-1430')
    data = c.readFrame()
    print(data)

