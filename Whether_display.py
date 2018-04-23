import glob
import json
import requests
import sched
import time
import tkinter as tk
from tkinter import ttk, PhotoImage, Frame
import webbrowser
# This loads the DarkSkyConfig.py values
import DarkSkyConfig

class Window(ttk.Frame):

    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)               
        self.master = master
        self.loopcount = 24
        # Variables to use

        # Current variables
        self.timeText = tk.StringVar()
        self.timeText.set("00:00AM")
        self.currentPhotoImage = PhotoImage(file="images/cloudy.png")
        self.currentPhotoImageText = tk.StringVar()
        self.currentPhotoImageText.set("Null")
        self.currentTempText = tk.StringVar()
        self.currentTempText.set("0.0")
        self.apparentTempText = tk.StringVar()
        self.apparentTempText.set("(0.0)")
        self.currentSummeryText = tk.StringVar()
        self.currentSummeryText.set("Unknown")

        # Day 0 variables

        # Widgets

        # Frames
        self.nowFrame = Frame(root)
        self.daysFrame = Frame(root)
        self.day0Frame = Frame(root)
        self.day1Frame = Frame(root)
        self.day2Frame = Frame(root)
        self.day3Frame = Frame(root)
        self.day4Frame = Frame(root)

        # Current widgets
        # textvariable automatically updates with the StringVar() it's assigned to
        self.timeLabel = ttk.Label(self.nowFrame, textvariable=self.timeText, font=("arial", 40, "bold")).grid()
        self.currentIcon = ttk.Label(self.nowFrame, image=self.currentPhotoImage)
        self.currentIcon.grid(column=0, row=1)
        self.currentIconText = ttk.Label(self.nowFrame, textvariable=self.currentPhotoImageText, font=("arial", 21, "bold"))
        self.currentIconText.grid(column=0, row=2)
        self.currentTemp = ttk.Label(self.nowFrame, textvariable=self.currentTempText, font=("arial", 58, "bold"))
        self.currentTemp.grid(column=0, row=3)
        self.apparentTemp = ttk.Label(self.nowFrame, textvariable=self.apparentTempText, font=("arial", 12))
        self.apparentTemp.grid(column=0, row=4)
        self.currentSummery = ttk.Label(self.nowFrame, textvariable=self.currentSummeryText, font=("arial", 10), wraplength=300)
        self.currentSummery.grid(column=0, row=5)
        self.poweredBy = ttk.Label(self.nowFrame, text="Powered By DarkSky", font=("arial", 8), foreground="white", cursor="hand2")
        self.poweredBy.grid(column=0, row=6)
        self.poweredBy.bind("<Button-1>", openApiLink)

        # Day 0 variables

        # Setting the frames
        self.nowFrame.grid()


        
      

def DisUpdate():
    if app.loopcount == 24:
        VarSet()
    app.loopcount += 1
    # This displays the local time in a 12 hour format
    app.timeText.set(time.strftime("%I:%M%p"))
    root.update_idletasks()
    #This loops the current function after 5 seconds
    root.after(5000, DisUpdate)
    return()

def VarSet():
    app.loopcount = -1
    # Current values
    # Update the image by updating the variable then the label
    app.currentPhotoImage = PhotoImage(file="images/wind.png")
    app.currentIcon.configure(image=app.currentPhotoImage)
    app.currentTempText.set("888.88")
    app.apparentTempText.set("(888.88)")
    app.currentPhotoImageText.set("Not null")
    app.currentSummeryText.set("There may be rain within the hour, more details will be coming soon, please wait")

def openApiLink(event):
    webbrowser.open("https://darksky.net/poweredby/")

# Creating the window
root = tk.Tk()
app = Window(root)
app.master.title("Weather Display")
app.master.geometry("800x480")
root.minsize(800,480)
# Loads the DisUpdate function after loading the window
root.after(5000, DisUpdate)
root.mainloop()



#content = json.loads(requests.get("https://api.darksky.net/forecast/a29d6bfa474ca4788425d6e0303f472e/50.852836,0.558773?units=si").text)
#content = json.loads(open("darksky_file.json").read())
#print(content["minutely"]["icon"])
