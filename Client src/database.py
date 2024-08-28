import json

class Logger:
    def __init__(self, filepath):
        self.filepath = filepath
    def write(self, d):
        file = open(self.filepath, "a+")
        file.write(json.dumps(d) + "\n")
        file.close()
        #print(json.dumps(d))

class Reader:
    def __init__(self, filepath):
        self.file = open(filepath, "r")
    def __del__(self):
        self.file.close()
    def readpoint(self):
        x = self.file.readline()
        if x == '':
            return {}
        return json.loads(x)
    
class Database:
    @staticmethod
    def mapMacs(filename):
        mac_mappings={}
        r = Reader(filename)
        raw = r.readpoint()
        counter = 0
        while raw != {}:
            macs = list(raw.values())[0]
            # list of router macs
            for mac in macs.keys():
                if mac in mac_mappings.keys():
                    pass
                else:
                    mac_mappings[mac] = counter
                    counter+=1
            raw = r.readpoint()
        return mac_mappings

    @staticmethod
    def loadData(mappings, filename):
        trainset = []
        r = Reader(filename)
        raw = r.readpoint()
        while raw != {}:
            roomID = list(raw.keys())[0]
            _signals = list(raw.values())[0]
            signals = []
            for set in _signals.items():
                signals.append([mappings[set[0]], set[1]])
            trainset.append([int(roomID), signals])
            raw = r.readpoint()
        return trainset
    
    @staticmethod
    def loadEntries(filename):
        trainset = []
        r = Reader(filename)
        raw = r.readpoint()
        while raw != {}:
            trainset.append(raw)
            raw = r.readpoint()
        return trainset


    @staticmethod
    def transformLogEntry(entry, mappings, iodim):
        roomCode = int(list(entry.keys())[0])
        output = [1 if i+1 == roomCode else 0 for i in range(iodim[1])]
        input = [0 for i in range(iodim[0])]
        #print(list(entry.values())[0])
        #while True: pass
        for bssid, strength in list(entry.values())[0].items():
            #print(mappings[bssid])
            try:
                input[mappings[bssid]] = strength/255.0
            except:
                pass
        return (input, output)
    
    @staticmethod
    def stringify(mac):
        return hex(mac[0])[2::] + ":" + hex(mac[1])[2::] + ":" + hex(mac[2])[2::] + ":" + hex(mac[3])[2::] + ":" + hex(mac[4])[2::] + ":" + hex(mac[5])[2::]

    @staticmethod
    def framesToDict(frames):
        dict_frames = {}
        for frame in frames:
            dict_frames[Database.stringify(frame)] = frame[6]
        return {"-1":dict_frames}


if __name__ == '__main__':
    mappings = Database.mapMacs('logdata_2268')
    entries = Database.loadEntries('logdata_2268')
    entry = entries[0]
    inputs, outputs = Database.transformLogEntry(entry, mappings, (65, 7))
    print(inputs)