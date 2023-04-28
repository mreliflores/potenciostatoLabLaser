from .root import main
from .data import DataMaster
from .Serial_Ctrl import SerialCtrl
from .create import createCSV

def main_():
    data = DataMaster()
    serial = SerialCtrl()
    create = createCSV()
    app = main(serial, data, create)
    app.mainloop()