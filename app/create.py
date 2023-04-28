from tkinter.filedialog import asksaveasfilename
import csv

class createCSV():
    def __init__(self):
        self.file_obj = None
        pass
    pass

    def createPath(self, data):
        self.file_obj = asksaveasfilename(
            filetypes=[("CSV File", ".csv")],
            defaultextension=".csv",
            title="Save as"
        )

        if len(self.file_obj) > 0:
            with open(f'{self.file_obj}', 'w', newline='') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerows(zip(data.XData, data.YData))
                pass
            pass


if __name__ == "__main__":
    createCSV()