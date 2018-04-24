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
        self.day0NameText = tk.StringVar()
        self.day0NameText.set("Nul")
        self.day0PhotoImage = PhotoImage(file="images_small/cloudy.png")
        self.day0MinText = tk.StringVar()
        self.day0MinText.set("Min:\n00")
        self.day0MaxText = tk.StringVar()
        self.day0MaxText.set("Max:\n00")

        # Day 1 variables
        self.day1NameText = tk.StringVar()
        self.day1NameText.set("Nul")
        self.day1PhotoImage = PhotoImage(file="images_small/cloudy.png")

        # Day 2 variables
        self.day2NameText = tk.StringVar()
        self.day2NameText.set("Nul")
        self.day2PhotoImage = PhotoImage(file="images_small/cloudy.png")

        # Day 3 variables
        self.day3NameText = tk.StringVar()
        self.day3NameText.set("Nul")
        self.day3PhotoImage = PhotoImage(file="images_small/cloudy.png")

        # Day 4 variables
        self.day4NameText = tk.StringVar()
        self.day4NameText.set("Nul")
        self.day4PhotoImage = PhotoImage(file="images_small/cloudy.png")

        # Widgets

        # Frames
        self.nowFrame = Frame(root)
        self.daysFrame = Frame(root)
        self.day0Frame = Frame(self.daysFrame)
        self.day1Frame = Frame(self.daysFrame)
        self.day2Frame = Frame(self.daysFrame)
        self.day3Frame = Frame(self.daysFrame)
        self.day4Frame = Frame(self.daysFrame)

        # Current widgets
        # textvariable automatically updates with the StringVar() it's assigned to
        self.timeLabel = ttk.Label(self.nowFrame, textvariable=self.timeText, font=("arial", 40, "bold"))
        self.timeLabel.grid()
        self.currentPhoto = ttk.Label(self.nowFrame, image=self.currentPhotoImage)
        self.currentPhoto.grid(column=0, row=1)
        self.currentPhotoText = ttk.Label(self.nowFrame, textvariable=self.currentPhotoImageText, font=("arial", 21, "bold"))
        self.currentPhotoText.grid(column=0, row=2)
        self.currentTemp = ttk.Label(self.nowFrame, textvariable=self.currentTempText, font=("arial", 58, "bold"))
        self.currentTemp.grid(column=0, row=3)
        self.apparentTemp = ttk.Label(self.nowFrame, textvariable=self.apparentTempText, font=("arial", 12))
        self.apparentTemp.grid(column=0, row=4)
        self.currentSummery = ttk.Label(self.nowFrame, textvariable=self.currentSummeryText, font=("arial", 10), wraplength=300)
        self.currentSummery.grid(column=0, row=5)
        self.poweredBy = ttk.Label(self.nowFrame, text="Powered By DarkSky", font=("arial", 8), foreground="white", cursor="hand2")
        self.poweredBy.grid(column=0, row=6)
        self.poweredBy.bind("<Button-1>", openApiLink)

        # Day 0 widgets
        self.day0Name = ttk.Label(self.day0Frame, textvariable=self.day0NameText, font=("arial", 12, "bold"))
        self.day0Name.grid()
        self.day0Photo = ttk.Label(self.day0Frame, image=self.day0PhotoImage)
        self.day0Photo.grid(column=1, row=1)
        self.day0Max = ttk.Label(self.day0Frame, textvariable=self.day0MaxText, font=("arial", 18, "bold"))
        self.day0Max.grid(column=2, row=1, padx=10)
        self.day0Min = ttk.Label(self.day0Frame, textvariable=self.day0MinText, font=("arial", 18, "bold"))
        self.day0Min.grid(column=3, row=1, padx=10)

        # Day 1 widgets
        self.day1Name = ttk.Label(self.day1Frame, textvariable=self.day1NameText, font=("arial", 12, "bold"))
        self.day1Name.grid()
        self.day1Photo = ttk.Label(self.day1Frame, image=self.day1PhotoImage)
        self.day1Photo.grid(column=1)

        # Day 2 widgets
        self.day2Name = ttk.Label(self.day2Frame, textvariable=self.day2NameText, font=("arial", 12, "bold"))
        self.day2Name.grid()
        self.day2Photo = ttk.Label(self.day2Frame, image=self.day2PhotoImage)
        self.day2Photo.grid(column=1)

        # Day 3 widgets
        self.day3Name = ttk.Label(self.day3Frame, textvariable=self.day3NameText, font=("arial", 12, "bold"))
        self.day3Name.grid()
        self.day3Photo = ttk.Label(self.day3Frame, image=self.day3PhotoImage)
        self.day3Photo.grid(column=1)

        # Day 4 widgets
        self.day4Name = ttk.Label(self.day4Frame, textvariable=self.day4NameText, font=("arial", 12, "bold"))
        self.day4Name.grid()
        self.day4Photo = ttk.Label(self.day4Frame, image=self.day4PhotoImage)
        self.day4Photo.grid(column=1)


        # Setting the frames
        self.nowFrame.pack(side="left")
        self.daysFrame.pack(side="right", expand="true", fill="x")
        self.day0Frame.grid()
        self.day1Frame.grid(row=1)
        self.day2Frame.grid(row=2)
        self.day3Frame.grid(row=3)
        self.day4Frame.grid(row=4)


        
      

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
    app.currentPhoto.configure(image=app.currentPhotoImage)
    app.currentTempText.set("888.88")
    app.apparentTempText.set("(888.88)")
    app.currentPhotoImageText.set("Not null")
    app.currentSummeryText.set("There may be rain within the hour, more details will be coming soon, please wait")

    #Day0 values
    app.day0NameText.set("Tue")
    app.day0PhotoImage = PhotoImage(file="images_small/wind.png")
    app.day0Photo.configure(image=app.day0PhotoImage)
    app.day0MinText.set("Min:\n55")
    app.day0MaxText.set("Max:\n55")

    #Day1 values
    app.day1NameText.set("Wed")
    app.day1PhotoImage = PhotoImage(file="images_small/wind.png")
    app.day1Photo.configure(image=app.day1PhotoImage)

    #Day2 values
    app.day2NameText.set("Thr")
    app.day2PhotoImage = PhotoImage(file="images_small/wind.png")
    app.day2Photo.configure(image=app.day2PhotoImage)

    #Day3 values
    app.day3NameText.set("Fri")
    app.day3PhotoImage = PhotoImage(file="images_small/wind.png")
    app.day3Photo.configure(image=app.day3PhotoImage)

    #Day4 values
    app.day4NameText.set("Sat")
    app.day4PhotoImage = PhotoImage(file="images_small/wind.png")
    app.day4Photo.configure(image=app.day4PhotoImage)

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
