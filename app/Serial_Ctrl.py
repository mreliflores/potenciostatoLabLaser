from serial import Serial
import time

class SerialCtrl():
    def __init__(self):
        self.test_com = "?"
        self.sync_ok = "ok"
        pass

    def SerialOpen(self, app):
        try:
            self.ser.is_open
            pass
        except Exception as e:
            #print(e) debugging
            PORT = app.port.get()
            BAUD = 9600
            self.ser = Serial()
            self.ser.baudrate = BAUD
            self.ser.port = PORT
            self.ser.timeout = None
            pass

        try:
            if self.ser.is_open:
                self.ser.status = True
                pass
            else:
                PORT = app.port.get()
                BAUD = 9600
                self.ser = Serial()
                self.ser.baudrate = BAUD
                self.ser.port = PORT
                self.ser.timeout = None
                self.ser.open()
                self.ser.status = True
                pass
            pass
        except Exception as e:
            #print(e)
            self.ser.status = False
            pass
        pass

    def SerialClose(self):
        try:
            self.ser.is_open
            self.ser.close()
            self.ser.status = False
            pass
        except Exception as e:
            #rint(e)
            self.ser.status = False
            pass
        pass

    def SerialSync(self, COM, data):
        self.threading = True
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer
        time.sleep(2) #time to Arduino respond
        self.ser.write(self.test_com.encode())
        self.ser.reset_output_buffer()
        
        COM.connect_button["state"] = "active"              

        while self.threading:
            try:
                COM.sync["text"] = "...Sync..."
                COM.sync["fg"] = "orange"
                data.RowMsg = self.ser.readline()
                #print(f"Row: {data.RowMsg}")
                data.DecodeMsg()
                if self.sync_ok in data.msg[0]:
                    if COM.parent.tech.get()!=0:
                        COM.start_button["state"] = "active"
                        pass
                    COM.sync["text"] = "OK"
                    COM.sync["fg"] = "green"
                    self.threading = False
                    break
                if self.threading == False:
                    break
            except Exception as e:
                print('xx')
                print(e)
                pass
            if self.threading == False:
                break

        pass

    def serDataStream(self, COM, ENT, data, create):
        self.threading = True
        tech = COM.parent.tech.get()

        if tech == 1:
            t_stab = COM.parent.t_stab.get()
            E0 = COM.parent.E0.get()
            Ei = COM.parent.Ei.get()
            Ef = COM.parent.Ef.get()
            cyc_num = COM.parent.cyc_num.get()
            scan_rate = COM.parent.scan_rate.get()

            ENT.t_stab["state"] = "disable"
            ENT.E0["state"] = "disable"
            ENT.Ei["state"] = "disable"
            ENT.Ef["state"] = "disable"
            ENT.cyc_num["state"] = "disable"
            ENT.scan_rate["state"] = "disable"
            ENT.backButton["state"] = "disable"
        

            self.parametersToArduino = f"{tech}x{E0}x{Ei}x{Ef}x{cyc_num}x{scan_rate}x0x0x{t_stab}x"
            #print(self.parametersToArduino)
            self.ser.write(self.parametersToArduino.encode())
            pass

        elif tech == 2:
            E0 = COM.parent.E0.get()
            timeChrono = COM.parent.timeChrono.get()
            stepTime = COM.parent.stepTime.get()

            ENT.voltChrono["state"] = "disable"
            ENT.timeChrono["state"] = "disable"
            ENT.stepTime["state"] = "disable"
            ENT.backButton["state"] = "disable"

            self.parametersToArduino = f"{tech}x{E0}x0x0x0x0x{timeChrono}x{stepTime}x0x"
            self.ser.write(self.parametersToArduino.encode())
            pass

        elif tech == 3:
            t_stab = COM.parent.t_stab.get()
            Ei = COM.parent.Ei.get()
            Ef = COM.parent.Ef.get()
            cyc_num = COM.parent.cyc_num.get()
            scan_rate = COM.parent.scan_rate.get()

            ENT.t_stab["state"] = "disable"
            ENT.Ei["state"] = "disable"
            ENT.Ef["state"] = "disable"
            ENT.cyc_num["state"] = "disable"
            ENT.scan_rate["state"] = "disable"
            ENT.backButton["state"] = "disable"
        

            self.parametersToArduino = f"{tech}x0x{Ei}x{Ef}x{cyc_num}x{scan_rate}x0x0x{t_stab}x"
            #print(self.parametersToArduino)
            self.ser.write(self.parametersToArduino.encode())
            pass

        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()       
        COM.stop_button["state"] = "active"
        COM.UpdateChart()

        while self.threading and (tech==2):
            try:
                data.RowMsg = self.ser.readline()
                data.DecodeMsgC()
                if len(data.RowMsg)>0:
                    data.setRefTime()
                    data.upXTimedata()
                    data.upYData(tech)
                    break
                    pass
            except Exception as e:
                print(e)
                pass


        while self.threading and (tech==2):
            try:
                data.RowMsg = self.ser.readline()
                data.DecodeMsgC()
                if len(data.RowMsg)>0:
                    if b'N' in data.RowMsg:
                        ENT.voltChrono["state"] = "active"
                        ENT.timeChrono["state"] = "active"
                        ENT.stepTime["state"] = "active"
                        ENT.backButton["state"] = "active"
                        ENT.backButton["state"] = "active"
                        COM.start_button["state"] = "active"
                        COM.stop_button["state"] = "disable"

                        create.createPath(data)
                        
                        data.XData = []
                        data.YData = []
                        self.threading = False
                        break
                    data.upXTimedata()
                    data.upYData(tech)
                    pass
            except Exception as e:
                
                print(e)
                pass



        while self.threading and (not (tech==2)):
            try:
                read_ = True
                buffer = b''
                while read_:
                    # Leer lo que haya en el puerto (si no hay nada, sigue el loop)
                    chunk = self.ser.read()
                    buffer += chunk
                    if b'\r\n' in buffer:
                        read_ = False
                    # Mientras haya un mensaje completo en el buffer
                            
                data.RowMsg = buffer
                data.DecodeMsg()
                if len(data.RowMsg)>0:
                    if b'N' in data.RowMsg:
                        if tech == 1:
                            ENT.t_stab["state"] = "active"
                            ENT.E0["state"] = "active"
                            ENT.Ei["state"] = "active"
                            ENT.Ef["state"] = "active"
                            ENT.cyc_num["state"] = "active"
                            ENT.scan_rate["state"] = "active"
                            ENT.backButton["state"] = "active"
                            COM.start_button["state"] = "active"
                            COM.stop_button["state"] = "disable"
                        else:
                            ENT.t_stab["state"] = "active"
                            ENT.Ei["state"] = "active"
                            ENT.Ef["state"] = "active"
                            ENT.cyc_num["state"] = "active"
                            ENT.scan_rate["state"] = "active"
                            ENT.backButton["state"] = "active"
                            COM.start_button["state"] = "active"
                            COM.stop_button["state"] = "disable"

                        create.createPath(data)
                        
                        data.XData = []
                        data.YData = []
                        self.threading = False
                        break
                    data.upXData()
                    data.upYData(tech)
                    data.msg=[]
                    pass
                pass
            except Exception as e:
                #print('updateyDatsa')
                #print(e)
                pass





    

if __name__=="__main__":
    SerialCtrl()