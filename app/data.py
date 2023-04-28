import time

class DataMaster():
    def __init__(self):
        self.msg = []

        self.XData = []
        self.YData = []
        pass

    def DecodeMsg(self):
        temporal = self.RowMsg.decode('utf8')
        if ((len(temporal)>=14) and (len(temporal)<=20)) or (len(temporal)==5):
            if "x" in temporal:
                self.msg = temporal.split("x")
                del self.msg[-1]
                pass
            #print(self.msg) #debugg
            pass
        pass

    def DecodeMsgC(self):
        temporal = self.RowMsg.decode('utf8')
        if (len(temporal)>0):
            if "x" in temporal:
                self.msg = temporal.split("x")
                del self.msg[-1]
                pass
            #print(self.msg) #debugg
            pass
        pass

    def setRefTime(self):
        if len(self.XData) == 0:
            self.refTime = time.perf_counter()
        else:
            self.refTime = time.perf_counter() - self.XData[-1]
    
    def upXTimedata(self):
        if len(self.XData)==0:
            self.XData.append(0)
        else:
            self.XData.append(time.perf_counter() - self.refTime)

    def upXData(self):
        self.XData.append(float(self.msg[0]))


    def upYData(self, tech):
        if tech == 2:
            self.YData.append(float(self.msg[0]))
            pass
        else:
            self.YData.append(float(self.msg[1]))
            pass



if __name__ == "__main__":
    DataMaster()