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
# This loads the config values from other python files
import DarkSkyConfig
import Weather_Display_Config as ConfigSet


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
        self.currentSummaryText = tk.StringVar()
        self.currentSummaryText.set("Unknown")

        # Sun rise/set vars
        self.risePhotoImage = PhotoImage(file="images_small/sun-rise.png")
        self.setPhotoImage = PhotoImage(file="images_small/sun-set.png")

        # Day vars condenced
        self.daysVars = {}
        for i in range(0, 5):
            self.daysVars["day" + str(i)] = {}
            self.daysVars["day" + str(i)]["NameText"] = tk.StringVar()
            self.daysVars["day" + str(i)]["NameText"].set("Nul")
            self.daysVars["day" + str(i)]["PhotoImage"] = PhotoImage(file="images_small/cloudy.png")
            self.daysVars["day" + str(i)]["MinText"] = tk.StringVar()
            self.daysVars["day" + str(i)]["MinText"].set("Min:\n00")
            self.daysVars["day" + str(i)]["MaxText"] = tk.StringVar()
            self.daysVars["day" + str(i)]["MaxText"].set("Max:\n00")
            self.daysVars["day" + str(i)]["RiseText"] = tk.StringVar()
            self.daysVars["day" + str(i)]["RiseText"].set("00:00")
            self.daysVars["day" + str(i)]["SetText"] = tk.StringVar()
            self.daysVars["day" + str(i)]["SetText"].set("00:00")
            self.daysVars["day" + str(i)]["SummaryText"] = tk.StringVar()
            self.daysVars["day" + str(i)]["SummaryText"].set("Unknown")

        # Widgets

        # Frames
        self.nowFrame = Frame(root)
        self.daysFrame = Frame(root)
        self.daysFrameCollection = {}
        self.daysWidgetCollection = {}
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
        self.currentSummary = ttk.Label(self.nowFrame, textvariable=self.currentSummaryText, font=("arial", 10), wraplength=300)
        self.currentSummary.grid(column=0, row=5)
        self.poweredBy = ttk.Label(self.nowFrame, text="Powered By DarkSky", font=("arial", 8), foreground="white", cursor="hand2")
        self.poweredBy.grid(column=0, row=6)
        self.poweredBy.bind("<Button-1>", openApiLink)

        # Day widgets (condenced)
        for i in range(0, 5):
            self.daysFrameCollection["day" + str(i)] = Frame(self.daysFrame)
            self.daysWidgetCollection["day" + str(i)] = {}
            self.daysWidgetCollection["day" + str(i)]["Name"] = ttk.Label(self.daysFrameCollection["day" + str(i)], textvariable=self.daysVars["day" + str(i)]["NameText"], font=("arial", 12, "bold"))
            self.daysWidgetCollection["day" + str(i)]["Name"].grid()
            self.daysWidgetCollection["day" + str(i)]["Photo"] = ttk.Label(self.daysFrameCollection["day" + str(i)], image=self.daysVars["day" + str(i)]["PhotoImage"])
            self.daysWidgetCollection["day" + str(i)]["Photo"].grid(column=1, row=1, rowspan=2)
            self.daysWidgetCollection["day" + str(i)]["Max"] = ttk.Label(self.daysFrameCollection["day" + str(i)], textvariable=self.daysVars["day" + str(i)]["MaxText"], font=("arial", 18, "bold"))
            self.daysWidgetCollection["day" + str(i)]["Max"].grid(column=2, row=1, padx=10, rowspan=2)
            self.daysWidgetCollection["day" + str(i)]["Min"] = ttk.Label(self.daysFrameCollection["day" + str(i)], textvariable=self.daysVars["day" + str(i)]["MinText"], font=("arial", 18, "bold"))
            self.daysWidgetCollection["day" + str(i)]["Min"].grid(column=3, row=1, padx=10, rowspan=2)
            self.daysWidgetCollection["day" + str(i)]["RisePhoto"] = ttk.Label(self.daysFrameCollection["day" + str(i)], image=self.risePhotoImage)
            self.daysWidgetCollection["day" + str(i)]["RisePhoto"].grid(column=4, row=1, padx=5)
            self.daysWidgetCollection["day" + str(i)]["Rise"] = ttk.Label(self.daysFrameCollection["day" + str(i)], textvariable=self.daysVars["day" + str(i)]["RiseText"], font=("arial", 18, "bold"))
            self.daysWidgetCollection["day" + str(i)]["Rise"].grid(column=4, row=2, padx=5)
            self.daysWidgetCollection["day" + str(i)]["SetPhoto"] = ttk.Label(self.daysFrameCollection["day" + str(i)], image=self.setPhotoImage)
            self.daysWidgetCollection["day" + str(i)]["SetPhoto"].grid(column=5, row=1, padx=5)
            self.daysWidgetCollection["day" + str(i)]["Set"] = ttk.Label(self.daysFrameCollection["day" + str(i)], textvariable=self.daysVars["day" + str(i)]["SetText"], font=("arial", 18, "bold"))
            self.daysWidgetCollection["day" + str(i)]["Set"].grid(column=5, row=2, padx=5)
            self.daysWidgetCollection["day" + str(i)]["Summary"] = ttk.Label(self.daysFrameCollection["day" + str(i)], textvariable=self.daysVars["day" + str(i)]["SummaryText"], font=("arial", 8), wraplength=100)
            self.daysWidgetCollection["day" + str(i)]["Summary"].grid(column=6, row=0, rowspan=3)

        # Setting the frames
        self.nowFrame.pack(side="left")
        self.daysFrame.pack(side="right", expand="true")
        for i in range(0, 5):
            self.daysFrameCollection["day" + str(i)].grid(row=i)

        #Setting the background colour for all elements
        self.frameList = [self.nowFrame, self.daysFrame, self.daysFrameCollection["day0"], self.daysFrameCollection["day1"], self.daysFrameCollection["day2"], self.daysFrameCollection["day3"], self.daysFrameCollection["day4"]]
        for currentframe in self.frameList:
            currentframe.configure(background=ConfigSet.BGColor)
            for currentWidget in currentframe.winfo_children():
                currentWidget.configure(background=ConfigSet.BGColor)


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
    app.currentSummaryText.set(content["minutely"]["summary"])

    # Day values condenced
    for i in range(0, 5):
        app.daysVars["day" + str(i)]["NameText"].set(datetime.datetime.fromtimestamp(content["daily"]["data"][i]["time"]).strftime("%a"))
        app.daysVars["day" + str(i)]["PhotoImage"] = PhotoImage(file="images_small/" + content["daily"]["data"][i]["icon"] + ".png")
        app.daysWidgetCollection["day" + str(i)]["Photo"].configure(image=app.daysVars["day" + str(i)]["PhotoImage"])
        app.daysVars["day" + str(i)]["MinText"].set("Min:\n" + str(round(content["daily"]["data"][i]["temperatureLow"],roundto)))
        app.daysVars["day" + str(i)]["MaxText"].set("Max:\n" + str(round(content["daily"]["data"][i]["temperatureHigh"],roundto)))
        app.daysVars["day" + str(i)]["RiseText"].set(datetime.datetime.fromtimestamp(content["daily"]["data"][i]["sunriseTime"]).strftime("%I:%M"))
        app.daysVars["day" + str(i)]["SetText"].set(datetime.datetime.fromtimestamp(content["daily"]["data"][i]["sunsetTime"]).strftime("%I:%M"))
        app.daysVars["day" + str(i)]["SummaryText"].set(content["daily"]["data"][i]["summary"])

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
root.configure(background=ConfigSet.BGColor)
root.mainloop()
