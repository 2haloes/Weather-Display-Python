import datetime
import json
import os
import requests
import sys
from sys import argv
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
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
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

        # Sun rise/set vars
        self.risePhotoImage = PhotoImage(file="images_small/sun-rise.png")
        self.setPhotoImage = PhotoImage(file="images_small/sun-set.png")

        # Day 0 variables
        self.day0NameText = tk.StringVar()
        self.day0NameText.set("Nul")
        self.day0PhotoImage = PhotoImage(file="images_small/cloudy.png")
        self.day0MinText = tk.StringVar()
        self.day0MinText.set("Min:\n00")
        self.day0MaxText = tk.StringVar()
        self.day0MaxText.set("Max:\n00")
        self.day0RiseText = tk.StringVar()
        self.day0RiseText.set("00:00")
        self.day0SetText = tk.StringVar()
        self.day0SetText.set("00:00")
        self.day0SummeryText = tk.StringVar()
        self.day0SummeryText.set("Unknown")

        # Day 1 variables
        self.day1NameText = tk.StringVar()
        self.day1NameText.set("Nul")
        self.day1PhotoImage = PhotoImage(file="images_small/cloudy.png")
        self.day1MinText = tk.StringVar()
        self.day1MinText.set("Min:\n00")
        self.day1MaxText = tk.StringVar()
        self.day1MaxText.set("Max:\n00")
        self.day1RiseText = tk.StringVar()
        self.day1RiseText.set("00:00")
        self.day1SetText = tk.StringVar()
        self.day1SetText.set("00:00")
        self.day1SummeryText = tk.StringVar()
        self.day1SummeryText.set("Unknown")
        

        # Day 2 variables
        self.day2NameText = tk.StringVar()
        self.day2NameText.set("Nul")
        self.day2PhotoImage = PhotoImage(file="images_small/cloudy.png")
        self.day2MinText = tk.StringVar()
        self.day2MinText.set("Min:\n00")
        self.day2MaxText = tk.StringVar()
        self.day2MaxText.set("Max:\n00")
        self.day2RiseText = tk.StringVar()
        self.day2RiseText.set("00:00")
        self.day2SetText = tk.StringVar()
        self.day2SetText.set("00:00")
        self.day2SummeryText = tk.StringVar()
        self.day2SummeryText.set("Unknown")

        # Day 3 variables
        self.day3NameText = tk.StringVar()
        self.day3NameText.set("Nul")
        self.day3PhotoImage = PhotoImage(file="images_small/cloudy.png")
        self.day3MinText = tk.StringVar()
        self.day3MinText.set("Min:\n00")
        self.day3MaxText = tk.StringVar()
        self.day3MaxText.set("Max:\n00")
        self.day3RiseText = tk.StringVar()
        self.day3RiseText.set("00:00")
        self.day3SetText = tk.StringVar()
        self.day3SetText.set("00:00")
        self.day3SummeryText = tk.StringVar()
        self.day3SummeryText.set("Unknown")

        # Day 4 variables
        self.day4NameText = tk.StringVar()
        self.day4NameText.set("Nul")
        self.day4PhotoImage = PhotoImage(file="images_small/cloudy.png")
        self.day4MinText = tk.StringVar()
        self.day4MinText.set("Min:\n00")
        self.day4MaxText = tk.StringVar()
        self.day4MaxText.set("Max:\n00")
        self.day4RiseText = tk.StringVar()
        self.day4RiseText.set("00:00")
        self.day4SetText = tk.StringVar()
        self.day4SetText.set("00:00")
        self.day4SummeryText = tk.StringVar()
        self.day4SummeryText.set("Unknown")

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
        self.day0Photo.grid(column=1, row=1, rowspan=2)
        self.day0Max = ttk.Label(self.day0Frame, textvariable=self.day0MaxText, font=("arial", 18, "bold"))
        self.day0Max.grid(column=2, row=1, padx=10, rowspan=2)
        self.day0Min = ttk.Label(self.day0Frame, textvariable=self.day0MinText, font=("arial", 18, "bold"))
        self.day0Min.grid(column=3, row=1, padx=10, rowspan=2)
        self.day0RisePhoto = ttk.Label(self.day0Frame, image=self.risePhotoImage)
        self.day0RisePhoto.grid(column=4, row=1, padx=5)
        self.day0Rise = ttk.Label(self.day0Frame, textvariable=self.day0RiseText, font=("arial", 18, "bold"))
        self.day0Rise.grid(column=4, row=2, padx=5)
        self.day0SetPhoto = ttk.Label(self.day0Frame, image=self.setPhotoImage)
        self.day0SetPhoto.grid(column=5, row=1, padx=5)
        self.day0Set = ttk.Label(self.day0Frame, textvariable=self.day0SetText, font=("arial", 18, "bold"))
        self.day0Set.grid(column=5, row=2, padx=5)
        self.day0Summery = ttk.Label(self.day0Frame, textvariable=self.day0SummeryText, font=("arial", 8), wraplength=100)
        self.day0Summery.grid(column=6, row=0, rowspan=3)
        
        # Day 1 widgets
        self.day1Name = ttk.Label(self.day1Frame, textvariable=self.day1NameText, font=("arial", 12, "bold"))
        self.day1Name.grid()
        self.day1Photo = ttk.Label(self.day1Frame, image=self.day1PhotoImage)
        self.day1Photo.grid(column=1, row=1, rowspan=2)
        self.day1Max = ttk.Label(self.day1Frame, textvariable=self.day1MaxText, font=("arial", 18, "bold"))
        self.day1Max.grid(column=2, row=1, padx=10, rowspan=2)
        self.day1Min = ttk.Label(self.day1Frame, textvariable=self.day1MinText, font=("arial", 18, "bold"))
        self.day1Min.grid(column=3, row=1, padx=10, rowspan=2)
        self.day1RisePhoto = ttk.Label(self.day1Frame, image=self.risePhotoImage)
        self.day1RisePhoto.grid(column=4, row=1, padx=5)
        self.day1Rise = ttk.Label(self.day1Frame, textvariable=self.day1RiseText, font=("arial", 18, "bold"))
        self.day1Rise.grid(column=4, row=2, padx=5)
        self.day1SetPhoto = ttk.Label(self.day1Frame, image=self.setPhotoImage)
        self.day1SetPhoto.grid(column=5, row=1, padx=5)
        self.day1Set = ttk.Label(self.day1Frame, textvariable=self.day1SetText, font=("arial", 18, "bold"))
        self.day1Set.grid(column=5, row=2, padx=5)
        self.day1Summery = ttk.Label(self.day1Frame, textvariable=self.day1SummeryText, font=("arial", 8), wraplength=100)
        self.day1Summery.grid(column=6, row=0, rowspan=3)

        # Day 2 widgets
        self.day2Name = ttk.Label(self.day2Frame, textvariable=self.day2NameText, font=("arial", 12, "bold"))
        self.day2Name.grid()
        self.day2Photo = ttk.Label(self.day2Frame, image=self.day2PhotoImage)
        self.day2Photo.grid(column=1, row=1, rowspan=2)
        self.day2Max = ttk.Label(self.day2Frame, textvariable=self.day2MaxText, font=("arial", 18, "bold"))
        self.day2Max.grid(column=2, row=1, padx=10, rowspan=2)
        self.day2Min = ttk.Label(self.day2Frame, textvariable=self.day2MinText, font=("arial", 18, "bold"))
        self.day2Min.grid(column=3, row=1, padx=10, rowspan=2)
        self.day2RisePhoto = ttk.Label(self.day2Frame, image=self.risePhotoImage)
        self.day2RisePhoto.grid(column=4, row=1, padx=5)
        self.day2Rise = ttk.Label(self.day2Frame, textvariable=self.day2RiseText, font=("arial", 18, "bold"))
        self.day2Rise.grid(column=4, row=2, padx=5)
        self.day2SetPhoto = ttk.Label(self.day2Frame, image=self.setPhotoImage)
        self.day2SetPhoto.grid(column=5, row=1, padx=5)
        self.day2Set = ttk.Label(self.day2Frame, textvariable=self.day2SetText, font=("arial", 18, "bold"))
        self.day2Set.grid(column=5, row=2, padx=5)
        self.day2Summery = ttk.Label(self.day2Frame, textvariable=self.day2SummeryText, font=("arial", 8), wraplength=100)
        self.day2Summery.grid(column=6, row=0, rowspan=3)

        # Day 3 widgets
        self.day3Name = ttk.Label(self.day3Frame, textvariable=self.day3NameText, font=("arial", 12, "bold"))
        self.day3Name.grid()
        self.day3Photo = ttk.Label(self.day3Frame, image=self.day3PhotoImage)
        self.day3Photo.grid(column=1, row=1, rowspan=2)
        self.day3Max = ttk.Label(self.day3Frame, textvariable=self.day3MaxText, font=("arial", 18, "bold"))
        self.day3Max.grid(column=2, row=1, padx=10, rowspan=2)
        self.day3Min = ttk.Label(self.day3Frame, textvariable=self.day3MinText, font=("arial", 18, "bold"))
        self.day3Min.grid(column=3, row=1, padx=10, rowspan=2)
        self.day3RisePhoto = ttk.Label(self.day3Frame, image=self.risePhotoImage)
        self.day3RisePhoto.grid(column=4, row=1, padx=5)
        self.day3Rise = ttk.Label(self.day3Frame, textvariable=self.day3RiseText, font=("arial", 18, "bold"))
        self.day3Rise.grid(column=4, row=2, padx=5)
        self.day3SetPhoto = ttk.Label(self.day3Frame, image=self.setPhotoImage)
        self.day3SetPhoto.grid(column=5, row=1, padx=5)
        self.day3Set = ttk.Label(self.day3Frame, textvariable=self.day3SetText, font=("arial", 18, "bold"))
        self.day3Set.grid(column=5, row=2, padx=5)
        self.day3Summery = ttk.Label(self.day3Frame, textvariable=self.day3SummeryText, font=("arial", 8), wraplength=100)
        self.day3Summery.grid(column=6, row=0, rowspan=3)

        # Day 4 widgets
        self.day4Name = ttk.Label(self.day4Frame, textvariable=self.day4NameText, font=("arial", 12, "bold"))
        self.day4Name.grid()
        self.day4Photo = ttk.Label(self.day4Frame, image=self.day4PhotoImage)
        self.day4Photo.grid(column=1, row=1, rowspan=2)
        self.day4Max = ttk.Label(self.day4Frame, textvariable=self.day4MaxText, font=("arial", 18, "bold"))
        self.day4Max.grid(column=2, row=1, padx=10, rowspan=2)
        self.day4Min = ttk.Label(self.day4Frame, textvariable=self.day4MinText, font=("arial", 18, "bold"))
        self.day4Min.grid(column=3, row=1, padx=10, rowspan=2)
        self.day4RisePhoto = ttk.Label(self.day4Frame, image=self.risePhotoImage)
        self.day4RisePhoto.grid(column=4, row=1, padx=5)
        self.day4Rise = ttk.Label(self.day4Frame, textvariable=self.day4RiseText, font=("arial", 18, "bold"))
        self.day4Rise.grid(column=4, row=2, padx=5)
        self.day4SetPhoto = ttk.Label(self.day4Frame, image=self.setPhotoImage)
        self.day4SetPhoto.grid(column=5, row=1, padx=5)
        self.day4Set = ttk.Label(self.day4Frame, textvariable=self.day4SetText, font=("arial", 18, "bold"))
        self.day4Set.grid(column=5, row=2, padx=5)
        self.day4Summery = ttk.Label(self.day4Frame, textvariable=self.day4SummeryText, font=("arial", 8), wraplength=100)
        self.day4Summery.grid(column=6, row=0, rowspan=3)


        # Setting the frames
        self.nowFrame.pack(side="left")
        self.daysFrame.pack(side="right", expand="true")
        self.day0Frame.grid()
        self.day1Frame.grid(row=1)
        self.day2Frame.grid(row=2)
        self.day3Frame.grid(row=3)
        self.day4Frame.grid(row=4)

        #Setting the background colour for all elements
        self.frameList = [self.nowFrame, self.daysFrame, self.day0Frame, self.day1Frame, self.day2Frame, self.day3Frame, self.day4Frame]
        for currentframe in self.frameList:
            currentframe.configure(background="cyan")
            for currentWidget in currentframe.winfo_children():
                currentWidget.configure(background="cyan")


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
    # This attempts to get the data, if it fails, it tries again on the next loop around
    try:
        #content = json.loads(open("darksky_file.json").read())
        content = json.loads(requests.get("https://api.darksky.net/forecast/" + DarkSkyConfig.ApiKey + "/" + DarkSkyConfig.Lat + "," + DarkSkyConfig.Long + "?units=" + DarkSkyConfig.Units).text)
        tempMeasurement = ""
        roundto = 0
        if content["flags"]["units"] == "us":
            tempMeasurement = "°F"
            roundto = 0
        else:
            tempMeasurement = "°C"
            roundto = 1
    except:
        return
    # Current values
    # Update the image by updating the variable then the label
    app.currentPhotoImage = PhotoImage(file="images/"+ content["currently"]["icon"] +".png")
    app.currentPhoto.configure(image=app.currentPhotoImage)
    app.currentTempText.set(str(round(content["currently"]["temperature"],roundto)) + tempMeasurement)
    app.apparentTempText.set(str(round(content["currently"]["apparentTemperature"],roundto)) + tempMeasurement)
    app.currentPhotoImageText.set(content["currently"]["icon"])
    app.currentSummeryText.set(content["minutely"]["summary"])

    #Day0 values
    app.day0NameText.set(datetime.datetime.fromtimestamp(content["daily"]["data"][0]["time"]).strftime("%a"))
    app.day0PhotoImage = PhotoImage(file="images_small/" + content["daily"]["data"][0]["icon"] + ".png")
    app.day0Photo.configure(image=app.day0PhotoImage)
    app.day0MinText.set("Min:\n" + str(round(content["daily"]["data"][0]["temperatureLow"],roundto)))
    app.day0MaxText.set("Max:\n" + str(round(content["daily"]["data"][0]["temperatureHigh"],roundto)))
    app.day0RiseText.set(datetime.datetime.fromtimestamp(content["daily"]["data"][0]["sunriseTime"]).strftime("%I:%M"))
    app.day0SetText.set(datetime.datetime.fromtimestamp(content["daily"]["data"][0]["sunsetTime"]).strftime("%I:%M"))
    app.day0SummeryText.set(content["daily"]["data"][0]["summary"])

    #Day1 values
    app.day1NameText.set(datetime.datetime.fromtimestamp(content["daily"]["data"][1]["time"]).strftime("%a"))
    app.day1PhotoImage = PhotoImage(file="images_small/" + content["daily"]["data"][1]["icon"] + ".png")
    app.day1Photo.configure(image=app.day1PhotoImage)
    app.day1MinText.set("Min:\n" + str(round(content["daily"]["data"][1]["temperatureLow"],roundto)))
    app.day1MaxText.set("Max:\n" + str(round(content["daily"]["data"][1]["temperatureHigh"],roundto)))
    app.day1RiseText.set(datetime.datetime.fromtimestamp(content["daily"]["data"][1]["sunriseTime"]).strftime("%I:%M"))
    app.day1SetText.set(datetime.datetime.fromtimestamp(content["daily"]["data"][1]["sunsetTime"]).strftime("%I:%M"))
    app.day1SummeryText.set(content["daily"]["data"][1]["summary"])

    #Day2 values
    app.day2NameText.set(datetime.datetime.fromtimestamp(content["daily"]["data"][2]["time"]).strftime("%a"))
    app.day2PhotoImage = PhotoImage(file="images_small/" + content["daily"]["data"][2]["icon"] + ".png")
    app.day2Photo.configure(image=app.day2PhotoImage)
    app.day2MinText.set("Min:\n" + str(round(content["daily"]["data"][2]["temperatureLow"],roundto)))
    app.day2MaxText.set("Max:\n" + str(round(content["daily"]["data"][2]["temperatureHigh"],roundto)))
    app.day2RiseText.set(datetime.datetime.fromtimestamp(content["daily"]["data"][2]["sunriseTime"]).strftime("%I:%M"))
    app.day2SetText.set(datetime.datetime.fromtimestamp(content["daily"]["data"][2]["sunsetTime"]).strftime("%I:%M"))
    app.day2SummeryText.set(content["daily"]["data"][2]["summary"])

    #Day3 values
    app.day3NameText.set(datetime.datetime.fromtimestamp(content["daily"]["data"][3]["time"]).strftime("%a"))
    app.day3PhotoImage = PhotoImage(file="images_small/" + content["daily"]["data"][3]["icon"] + ".png")
    app.day3Photo.configure(image=app.day3PhotoImage)
    app.day3MinText.set("Min:\n" + str(round(content["daily"]["data"][3]["temperatureLow"],roundto)))
    app.day3MaxText.set("Max:\n" + str(round(content["daily"]["data"][3]["temperatureHigh"],roundto)))
    app.day3RiseText.set(datetime.datetime.fromtimestamp(content["daily"]["data"][3]["sunriseTime"]).strftime("%I:%M"))
    app.day3SetText.set(datetime.datetime.fromtimestamp(content["daily"]["data"][3]["sunsetTime"]).strftime("%I:%M"))
    app.day3SummeryText.set(content["daily"]["data"][3]["summary"])

    #Day4 values
    app.day4NameText.set(datetime.datetime.fromtimestamp(content["daily"]["data"][4]["time"]).strftime("%a"))
    app.day4PhotoImage = PhotoImage(file="images_small/" + content["daily"]["data"][4]["icon"] + ".png")
    app.day4Photo.configure(image=app.day4PhotoImage)
    app.day4MinText.set("Min:\n" + str(round(content["daily"]["data"][4]["temperatureLow"],roundto)))
    app.day4MaxText.set("Max:\n" + str(round(content["daily"]["data"][4]["temperatureHigh"],roundto)))
    app.day4RiseText.set(datetime.datetime.fromtimestamp(content["daily"]["data"][4]["sunriseTime"]).strftime("%I:%M"))
    app.day4SetText.set(datetime.datetime.fromtimestamp(content["daily"]["data"][4]["sunsetTime"]).strftime("%I:%M"))
    app.day4SummeryText.set(content["daily"]["data"][4]["summary"])

def openApiLink(event):
    webbrowser.open("https://darksky.net/poweredby/")

# Creating the window
root = tk.Tk()
app = Window(root)
app.master.title("Weather Display")
if "-f" in argv:
    root.attributes("-fullscreen", True)
else:
    app.master.geometry("800x480")
    root.minsize(800,480)
# Loads the DisUpdate function after loading the window
root.after(5000, DisUpdate)
root.configure(background="cyan")
root.mainloop()
