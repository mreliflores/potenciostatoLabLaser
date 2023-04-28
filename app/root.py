import threading
from .data import DataMaster #.
from .Serial_Ctrl import SerialCtrl #.
import tkinter as tk
from tkinter import ttk
from serial.tools import list_ports
from tkinter import messagebox
from .create import createCSV #.

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.figure import SubplotParams

class main(tk.Tk):
    def __init__(self, serial, data, create) -> None:
        super().__init__()
        self.serial = serial
        self.data = data
        self.create = create

        #self.withdraw()

        self.wm_title("Potentiostat: Cyclic Voltammetry")
        self.minsize(720,410)
        self.padx = 5
        self.pady = 5

        #Variables para enviar a arduino
        self.tech = tk.IntVar()
        self.t_stab = tk.IntVar()
        self.E0 = tk.IntVar()
        self.Ei = tk.IntVar()
        self.Ef = tk.IntVar()
        self.cyc_num = tk.IntVar()
        self.scan_rate = tk.IntVar()
        self.stepTime = tk.IntVar()
        self.timeChrono = tk.IntVar()
        self.t_stab.set(100)
        self.E0.set(100)
        self.Ei.set(-100)
        self.Ef.set(700)
        self.cyc_num.set(3)
        self.scan_rate.set(100)
        self.stepTime.set(1)
        self.timeChrono.set(50)
        #/////////////////////////////////

        self.port = tk.StringVar()

        self.lego()
        #self.NAME = NAME(self)
        self.ENT = ENT(self)
        self.COM = COM(self)

        self.protocol(
            "WM_DELETE_WINDOW",
            self.close_window
        )

    def close_window(self):
        print("Close the window")
        self.destroy()
        self.serial.threading = False

        plt.close()

        try:
            #self.serial.ser.write(self.data.off.encode())
            self.serial.SerialClose(self)
        except:
            pass

    def lego(self):
        #//////Frames
        #self.name_file = ttk.Frame(self)
        self.com_manager = ttk.Frame(self) #choose COM ports
        self.parameters = ttk.Frame(self) #inputs
        self.plot = ttk.Frame(self)  #plot area

        """self.name_file.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=self.padx,
            pady=self.pady,
            sticky=(tk.W+tk.E)
        )"""

        self.parameters.grid(
            row=0,
            column=0,
            padx=self.padx,
            pady=self.pady,
            sticky=(tk.N+tk.S+tk.W+tk.E)
        )

        self.com_manager.grid(
            row=1,
            column=0,
            padx=self.padx,
            pady=self.pady,
            sticky=(tk.N+tk.S+tk.W+tk.E)
        )

        self.plot.grid(
            row=0,
            column=1,
            padx=self.padx,
            pady=self.pady,
            sticky=(tk.N+tk.S+tk.W+tk.E),
            rowspan=2
        )

        #self.name_file.columnconfigure(0, weight=1)
        self.com_manager.columnconfigure(0, weight=1)
        self.com_manager.rowconfigure(0, weight=1)
        self.parameters.rowconfigure(0, weight=1)
        self.parameters.columnconfigure(0, weight=1)
        self.plot.rowconfigure(0, weight=1)

"""
class NAME(ttk.Frame):
    def __init__(self, parent):
        super().__init__
        self.parent = parent

        self.name_project = ttk.LabelFrame(
            master=self.parent.name_file,
            text="Name of the project"
        )

        self.entry_name = ttk.Entry(
            master=self.name_project,
            textvariable=self.parent.name_project,
            justify='left',
            takefocus='all'
        )

        self.button = ttk.Button(
            master=self.name_project,
            text="None",
            command=self.parent.create.createPath
        )

        self.name_project.grid(
            row=0,
            column=0,
            sticky=(tk.W+tk.E)
        )

        self.entry_name.grid(
            row=0,
            column=0,
            sticky='ew',
            ipady=1,
            padx=self.parent.padx,
            pady=self.parent.pady
        )

        self.button.grid(
            row=0,
            column=1,
            padx=self.parent.padx,
            pady=self.parent.pady
        )

        self.name_project.columnconfigure(0,weight=1)
        pass
    """


class COM(ttk.Frame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.chartMaster = CHART(self.parent)

        self.padx=30
        self.pady=5

        self.set_com = ttk.LabelFrame(
            master = self.parent.com_manager,
            text = "Comunication Manager"
        )

        self.ports_ = ttk.Label(
            master=self.set_com,
            text="Ports:"
        )

        self.ports = ttk.Combobox(
            master=self.set_com,
            textvariable=self.parent.port,
            values=self.Get_coms(),
            justify=tk.CENTER,
            state='readonly',
            width=28,
            postcommand=lambda: self.ports.configure(
               values=self.Get_coms() 
            )
        )

        self.connect_button = ttk.Button(
            master=self.set_com,
            text="Connect",
            #state="disable"
            command=self.serial_connect,#self.chartMaster.AddGraph,
            width=15
        )

        self.sync = tk.Label(
            master=self.set_com,
            text="...Sync...",
            fg="orange"
        )

        self.start_button = ttk.Button(
            master=self.set_com,
            text="Start",
            state="disable",
            command=self.startButton
        )

        self.stop_button = ttk.Button(
            master=self.set_com,
            text="Stop",
            state="disable",
            command=self.stopButton
        )
        
        self.set_com.grid(
            row=0,
            column=0,
            sticky=(tk.N+tk.S+tk.W+tk.E)
        )

        self.ports_.grid(
            row=0,
            column=0,
            padx=20,
            pady=self.pady,
            sticky=(tk.W+tk.E)
        )
        self.ports.grid(
            row=0,
            column=1,
            padx=5,
            pady=self.pady,
            sticky=(tk.W+tk.E),
            columnspan=2
        )

        self.connect_button.grid(
            row=1,
            column=0,
            padx=5,
            pady=self.pady-3,
            sticky=(tk.W+tk.E)
        )

        self.sync.grid(
            row=1,
            column=1
        )

        self.start_button.grid(
            row=1,
            column=2,
            padx=5,
            pady=self.pady-3,
            sticky=(tk.W+tk.E)
        )

        self.stop_button.grid(
            row=2,
            column=0,
            columnspan=3,
            padx=5,
            pady=self.pady-3,
            sticky=(tk.W+tk.E)
        )

        self.connect_button.columnconfigure(0, weight=1)


    def Get_coms(self):
        self.list_ports = list_ports.comports()
        self.coms = [com[0] for com in self.list_ports]
        self.coms.insert(0, "None")

        self.parent.port.set(self.coms[0])
        return self.coms

    def serial_connect(self):
        if self.connect_button["text"] in "Connect":
            #Start opening connection
            self.parent.serial.SerialOpen(self.parent)
            if self.parent.serial.ser.status:
                self.chartMaster.AddGraph()
                self.connect_button["text"] = "Disconnect"
                self.connect_button["state"] = "disable"
                self.ports["state"] = "disable"
                InfoMessage = f"Succesful UART connection using {self.ports.get()}"
                messagebox.showinfo("State of connection", InfoMessage)

                self.parent.serial.t1 = threading.Thread(
                    target=self.parent.serial.SerialSync,
                    args=(self, self.parent.data),
                    daemon=True
                )

                self.parent.serial.t1.start()

                pass
            else:
                ErrorMessage = f"Failure to establish UART connection using {self.ports.get()}"
                messagebox.showerror("Error connection", ErrorMessage)
        else:
            self.parent.serial.threading = False
            self.parent.serial.SerialClose()

            InfoMessage = f"UART connection using {self.ports.get()} is now closed"
            messagebox.showinfo("State of connection", InfoMessage)
            self.connect_button["text"] = "Connect"
            self.ports["state"] = "active"
            self.sync["text"] = "...Sync..."
            self.sync["fg"] = "orange"
            self.start_button["state"] = "disable"
            plt.close()
            pass
        pass

    def startButton(self):
        self.start_button["state"] = "disable"
        self.parent.serial.t2 = threading.Thread(
            target=self.parent.serial.serDataStream,
            args=(
                self,
                self.parent.ENT,
                self.parent.data,
                self.parent.create,
            ),
            daemon=True
        )

        self.parent.serial.t2.start()
        pass

    def stopButton(self):
        self.parametersToArduino = f"0x0x0x0x0x0x0x0x0x"
        self.parent.serial.threading = False
        self.parent.serial.ser.write(self.parametersToArduino.encode())
        self.start_button["state"] = "active"
        self.stop_button["state"] = "disable"

        self.parent.data.XData = []
        self.parent.data.YData = []

        if self.parent.tech.get() == 1:
            self.parent.ENT.t_stab["state"] = "active"
            self.parent.ENT.E0["state"] = "active"
            self.parent.ENT.Ei["state"] = "active"
            self.parent.ENT.Ef["state"] = "active"
            self.parent.ENT.cyc_num["state"] = "active"
            self.parent.ENT.scan_rate["state"] = "active"
            self.parent.ENT.backButton["state"] = "active"
            pass

        elif self.parent.tech.get() == 3:
            self.parent.ENT.t_stab["state"] = "active"
            self.parent.ENT.Ei["state"] = "active"
            self.parent.ENT.Ef["state"] = "active"
            self.parent.ENT.cyc_num["state"] = "active"
            self.parent.ENT.scan_rate["state"] = "active"
            self.parent.ENT.backButton["state"] = "active"
            pass
        pass

    def UpdateChart(self):
        try:
            self.X = self.parent.data.XData
            self.Y = self.parent.data.YData

            self.chartMaster.ax.set_ylabel(r'Current ($\mu$A)')
            self.chartMaster.ax.set_xlabel("Voltage (V)")
            self.chartMaster.ax.grid(color="blue", alpha=1, linestyle="dotted")
            self.chartMaster.ax.set_facecolor("w")
            self.chartMaster.ax.patch.set_facecolor("#FAFAFA")

            self.chartMaster.ax.scatter(
                self.X, self.Y, s=1.5, color='black'
            )
            self.chartMaster.fig.canvas.draw()
            self.chartMaster.ax.clear()
            pass

        except Exception as e:
            #print('updatechart')
            #print(e)
            pass

        if self.parent.serial.threading:
            self.parent.after(100, self.UpdateChart)
        pass

class ENT(ttk.Frame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.padx=5
        self.pady=5

        self.entries = ttk.LabelFrame(
            self.parent.parameters,
            text="Electrochemical Techniques"
        )

        self.entries.grid(row=0, column=0, sticky=(tk.W+tk.E+tk.N+tk.S))
        self.entries.columnconfigure(0, weight=1)

        self.setTech()

    def setEntriesCycV(self):
        if self.parent.COM.sync["text"] != "...Sync...":
            self.parent.COM.start_button["state"] = "active"
            pass
        self.parent.tech.set(1)

        for widget in self.entries.winfo_children():
            widget.destroy()
            pass

        self.entries["text"] = "Parameters"

        self.t_stab_ = ttk.Label(
            master = self.entries,
            text='Equilibrium time (ms):'
        )

        self.t_stab = ttk.Entry(
            master=self.entries,
            textvariable=self.parent.t_stab,
            justify='center'
        )

        self.E0_ = ttk.Label(
            master = self.entries,
            text='Starting Voltage (mV):'
        )

        self.E0 = ttk.Entry(
            master=self.entries,
            textvariable=self.parent.E0,
            justify='center'
        )

        self.Ei_ = ttk.Label(
            master = self.entries,
            text='Minimum Voltage (mV):'
        )

        self.Ei = ttk.Entry(
            master=self.entries,
            textvariable=self.parent.Ei,
            justify='center'
        )

        self.Ef_ = ttk.Label(
            master = self.entries,
            text='Maximum Voltage (mV):'
        )

        self.Ef = ttk.Entry(
            master=self.entries,
            textvariable=self.parent.Ef,
            justify='center'
        )

        self.cyc_num_ = ttk.Label(
            master = self.entries,
            text='Cycle Number:'
        )

        self.cyc_num = ttk.Entry(
            master=self.entries,
            textvariable=self.parent.cyc_num,
            justify='center'
        )

        self.scan_rate_ = ttk.Label(
            master = self.entries,
            text='Scan Rate (mV/s):'
        )

        self.scan_rate = ttk.Entry(
            master=self.entries,
            textvariable=self.parent.scan_rate,
            justify='center'
        )

        a = 'Note:'
        b = '- Max Voltage must be greater than Min Voltage.'
        c = '- Express voltage in milivolts'
        d = '- Only numbers'

        self.note=ttk.Label(
            master=self.entries,
            text=(
                a + '\n ' + b + '\n ' + c + '\n ' + d
            ),
            justify="left"
        )

        self.backButton = ttk.Button(
            master=self.entries,
            text="Back",
            command=self.back
        )

        self.t_stab_.grid(row=0, column=0, padx=self.padx+18, pady=self.pady)
        self.t_stab.grid(row=0, column=1, padx=self.padx, pady=self.pady)

        self.E0_.grid(row=1, column=0, padx=self.padx+18, pady=self.pady)
        self.E0.grid(row=1, column=1, padx=self.padx, pady=self.pady)

        self.Ei_.grid(row=2, column=0, padx=self.padx+18, pady=self.pady)
        self.Ei.grid(row=2, column=1, padx=self.padx, pady=self.pady)

        self.Ef_.grid(row=3, column=0, padx=self.padx+18, pady=self.pady)
        self.Ef.grid(row=3, column=1, padx=self.padx, pady=self.pady)

        self.cyc_num_.grid(row=4, column=0, padx=self.padx+18, pady=self.pady)
        self.cyc_num.grid(row=4, column=1, padx=self.padx, pady=self.pady)

        self.scan_rate_.grid(row=5, column=0, padx=self.padx+18, pady=self.pady)
        self.scan_rate.grid(row=5, column=1, padx=self.padx, pady=self.pady)

        self.note.grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=8)

        self.backButton.grid(
            row=7,
            column=1,
            sticky=(tk.E+tk.W),
            padx=5,
            pady=4
        )
        pass

    def setEntriesChrono(self):
        if self.parent.COM.sync["text"] != "...Sync...":
            self.parent.COM.start_button["state"] = "active"
            pass

        self.parent.tech.set(2)
        self.parent.E0.set(500)
        self.parent.timeChrono.set(100)
        self.parent.stepTime.set(1)

        for widget in self.entries.winfo_children():
            widget.destroy()
            pass

        self.entries["text"] = "Parameters"

        self.voltChrono_ = ttk.Label(
            master = self.entries,
            text='Voltage (mV):'
        )

        self.voltChrono = ttk.Entry(
            master=self.entries,
            textvariable=self.parent.E0,
            justify='center'
        )

        self.timeChrono_ = ttk.Label(
            master = self.entries,
            text='Time (s):'
        )

        self.timeChrono = ttk.Entry(
            master=self.entries,
            textvariable=self.parent.timeChrono,
            justify='center'
        )

        self.stepTime_ = ttk.Label(
            master = self.entries,
            text='Step time (s):'
        )

        self.stepTime = ttk.Entry(
            master=self.entries,
            textvariable=self.parent.stepTime,
            justify='center'
        )


        a = 'Note:'
        b = '- Express time in seconds.'
        c = '- Express voltage in milivolts'
        d = '- Only numbers'

        self.note=ttk.Label(
            master=self.entries,
            text=(
                a + '\n ' + b + '\n ' + c + '\n ' + d
            ),
            justify="left"
        )

        self.backButton = ttk.Button(
            master=self.entries,
            text="Back",
            command=self.back
        )

        self.voltChrono_.grid(row=0, column=0, padx=self.padx+18, pady=self.pady)
        self.voltChrono.grid(row=0, column=1, padx=self.padx, pady=self.pady)

        self.timeChrono_.grid(row=1, column=0, padx=self.padx+18, pady=self.pady)
        self.timeChrono.grid(row=1, column=1, padx=self.padx, pady=self.pady)

        self.stepTime_.grid(row=2, column=0, padx=self.padx+18, pady=self.pady)
        self.stepTime.grid(row=2, column=1, padx=self.padx, pady=self.pady)

        self.note.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=8)

        self.backButton.grid(
            row=4,
            column=1,
            sticky=(tk.E+tk.W),
            padx=5,
            pady=4
        )
        pass

    def setEntriesLinSweVolt(self):
        if self.parent.COM.sync["text"] != "...Sync...":
            self.parent.COM.start_button["state"] = "active"
            pass

        self.parent.tech.set(3)

        for widget in self.entries.winfo_children():
            widget.destroy()
            pass

        self.entries["text"] = "Parameters"

        self.t_stab_ = ttk.Label(
            master = self.entries,
            text='Equilibrium time (ms):'
        )

        self.t_stab = ttk.Entry(
            master=self.entries,
            textvariable=self.parent.t_stab,
            justify='center'
        )

        self.Ei_ = ttk.Label(
            master = self.entries,
            text='Minimum Voltage (mV):'
        )

        self.Ei = ttk.Entry(
            master=self.entries,
            textvariable=self.parent.Ei,
            justify='center'
        )

        self.Ef_ = ttk.Label(
            master = self.entries,
            text='Maximum Voltage (mV):'
        )

        self.Ef = ttk.Entry(
            master=self.entries,
            textvariable=self.parent.Ef,
            justify='center'
        )

        self.cyc_num_ = ttk.Label(
            master = self.entries,
            text='Cycle Number:'
        )

        self.cyc_num = ttk.Entry(
            master=self.entries,
            textvariable=self.parent.cyc_num,
            justify='center'
        )

        self.scan_rate_ = ttk.Label(
            master = self.entries,
            text='Scan Rate (mV/s):'
        )

        self.scan_rate = ttk.Entry(
            master=self.entries,
            textvariable=self.parent.scan_rate,
            justify='center'
        )

        a = 'Note:'
        b = '- Max Voltage must be greater than Min Voltage.'
        c = '- Express voltage in milivolts'
        d = '- Only numbers'

        self.note=ttk.Label(
            master=self.entries,
            text=(
                a + '\n ' + b + '\n ' + c + '\n ' + d
            ),
            justify="left"
        )

        self.backButton = ttk.Button(
            master=self.entries,
            text="Back",
            command=self.back
        )

        self.t_stab_.grid(row=0, column=0, padx=self.padx+18, pady=self.pady)
        self.t_stab.grid(row=0, column=1, padx=self.padx, pady=self.pady)

        self.Ei_.grid(row=2, column=0, padx=self.padx+18, pady=self.pady)
        self.Ei.grid(row=2, column=1, padx=self.padx, pady=self.pady)

        self.Ef_.grid(row=3, column=0, padx=self.padx+18, pady=self.pady)
        self.Ef.grid(row=3, column=1, padx=self.padx, pady=self.pady)

        self.cyc_num_.grid(row=4, column=0, padx=self.padx+18, pady=self.pady)
        self.cyc_num.grid(row=4, column=1, padx=self.padx, pady=self.pady)

        self.scan_rate_.grid(row=5, column=0, padx=self.padx+18, pady=self.pady)
        self.scan_rate.grid(row=5, column=1, padx=self.padx, pady=self.pady)

        self.note.grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=8)

        self.backButton.grid(
            row=7,
            column=1,
            sticky=(tk.E+tk.W),
            padx=5,
            pady=4
        )
        pass

    def back(self):
        self.parent.COM.start_button["state"] = "disable"
        self.setTech()
        pass

    def setTech(self):

        self.parent.tech.set(0)

        for widget in self.entries.winfo_children():
            widget.destroy()
            pass
        self.entries["text"] = "Electrochemical Techniques"

        self.chronoTech = ttk.Button(
            master=self.entries,
            text="Chronoamperometry",
            command=self.setEntriesChrono
        )

        self.linearTech = ttk.Button(
            master=self.entries,
            text="Linear Voltammetry",
            command= self.setEntriesLinSweVolt
        )

        self.voltATech = ttk.Button(
            master=self.entries,
            text="Cyc. Voltammetry",
            command=self.setEntriesCycV
        )

        self.chronoTech.grid(
            row=0,
            column=0,
            sticky=(tk.W+tk.E),
            pady=15,
            padx=15
        )

        self.linearTech.grid(
            row=1,
            column=0,
            sticky=(tk.W+tk.E),
            pady=15,
            padx=15
        )

        self.voltATech.grid(
            row=2,
            column=0,
            sticky=(tk.W+tk.E),
            pady=15,
            padx=15
        )
        pass


class CHART(ttk.Frame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.plotting = ttk.LabelFrame(
            master = self.parent.plot,
            text = "Chart"
        )

        self.plotting.grid(
            row=0,
            column=0,
            rowspan=2,
            sticky=(tk.N+tk.S+tk.W+tk.E)
        )

    def AddGraph(self):
        self.fig, self.ax = plt.subplots(
            figsize=(7.5, 4),
            dpi=100,
            constrained_layout=True,
            subplotpars=SubplotParams(left=0.1, bottom=0.1, right=0.95, top=0.95)
        )

        self.ax.set_ylabel(r'Current ($\mu$A)')
        self.ax.set_xlabel("Voltage (V)")
        self.ax.set_xlim(
            self.parent.Ei.get()/1000-0.1,
            self.parent.Ef.get()/1000+0.1
        )
        self.ax.grid(color="blue", alpha=1, linestyle="dotted")
        self.ax.set_facecolor("w")
        self.ax.patch.set_facecolor("#FAFAFA")

        self.canv = FigureCanvasTkAgg(self.fig, master=self.plotting)
        self.canv.get_tk_widget().grid(
            row=0,
            column=1,
            #ipadx=52,
            #ipady=24
        )



if __name__ == "__main__":
    data = DataMaster()
    serial = SerialCtrl()
    create = createCSV()
    app = main(serial, data, create)
    app.mainloop()

