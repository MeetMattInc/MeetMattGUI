
import time, vlc, json, requests, threading
from requests_oauthlib import OAuth1
from MediaPlayer import *
from Hue import *
from TrumpTweets import *
import requests as req
import subprocess

class IOTTrigger:
    def __init__(self):
        self.music = MediaPlayer()
        # self.lights = Hue()
        # self.trump = TrumpTweets()
        self.username = ''


    def lightsOff(self):
        self.lights.off()


    def lightsOn(self):
        self.lights.on()


    def partyMode(self):
        musicThread = threading.Thread(target=self.music.partyMode)
        lightThread = threading.Thread(target=self.lights.partyMode)

        musicThread.start()
        lightThread.start()


    def romanticMode(self):
        musicThread = threading.Thread(target=self.music.romanticMode)
        lightThread = threading.Thread(target=self.lights.romanticMode)

        musicThread.start()
        lightThread.start()
        # musicThread.join()


    def readTweet(self):
        self.lights.on()

        # trumpThread.daemon = True
        trumpThread = threading.Thread(target=self.trump.readTweet)

        trumpThread.start()

    def siriMode(self):
        subprocess.Popen('/Applications/Siri.app/Contents/MacOS/Siri')

    def profileName(self, username):

        if username == 'Marc':
            self.readTweet()

        elif username == 'Tian':
            self.partyMode()

        elif username == 'Anthony':
            self.romanticMode()

        elif username == 'Lucas':
            self.siriMode()



if __name__ == "__main__":

    trigger = IOTTrigger()
    # trigger.partyMode()
    # trigger.profileName('Anthony')
    # trigger.profileName('Tian')
    # trigger.profileName('Marc')
    trigger.profileName('Lucas')

