from app.root import main
from app.data import DataMaster
from app.Serial_Ctrl import SerialCtrl
from app.create import createCSV


data = DataMaster()
serial = SerialCtrl()
create = createCSV()
app = main(serial, data, create)
app.mainloop()