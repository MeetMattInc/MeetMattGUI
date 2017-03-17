# http://192.168.1.26/debug/clip.html
# http://169.254.146.153/debug/clip.html
# http://169.254.9.39/debug/clip.html'
# 0 to 65535
# https://www.meethue.com/api/nupnp
import vlc, time, json, os
import requests as req

class Hue:
    def __init__(self):
        import requests as req
        response = req.get('https://www.meethue.com/api/nupnp')
        self.IP = response.json()[0]['internalipaddress']
        self.USER = 'ESFCqAVx454fvbdJ8uayH3fLO8AOSrfMCtMtJN-f'
        self.BASE_URL = 'http://%s/api/%s/' % (self.IP, self.USER)

        self.bulb1 = self.BASE_URL + 'lights/1/state/'
        self.bulb2 = self.BASE_URL + 'lights/2/state/'
        self.bulb3 = self.BASE_URL + 'lights/3/state/'

        self.bulbs = [self.bulb1, self.bulb2, self.bulb3]

        # Colors
        self.WHITE = {"on":True, "sat":234, "bri":252,"hue":34768}
        self.RED = {"on":True, "sat":254, "bri":254,"hue":65534}
        self.GREEN = {"on":True, "sat":254, "bri":254,"hue":15000}
        self.BLUE = {"on":True, "sat":254, "bri":254,"hue":20000}


    def get(self):
        url = self.BASE_URL + 'lights'
        # url = 'https://www.meethue.com/api/nupnp'
        response = req.get(url)
        print(response.text)

    def put(self, bulbs, data):
        if type(bulbs) == str:
            response = req.put(bulbs, json=data)

        elif type(bulbs) == list:
            for bulb in bulbs:
                response = req.put(bulb, json=data)

        # if response.status_code != 200:
            # print("Put method failed")

    def off(self):
        data = {"on":False}
        self.put(self.bulbs, data)

    def on(self):
        data = {"on":True}
        self.put(self.bulbs, data)

    def partyMode(self):
        hue = [self.RED, self.BLUE, self.GREEN]
        data = {"on":True, "sat":254, "bri":254,"hue":20000}

        while data['hue'] < 65535:
            self.put(self.bulbs, data)
            data["hue"] += 3000
            time.sleep(0.5)
            self.off()
            time.sleep(0.5)

        self.off()

    def romanticMode(self):
        self.put(self.bulbs, self.RED)
        data1 = {"on":True, "sat":254, "bri":254,"hue":65534}
        data2 = {"on":True, "sat":254, "bri":0,"hue":65534}
        for i in range(8):
            self.put(self.bulbs, data1)
            time.sleep(1.8)
            self.put(self.bulbs, data2)
        self.off()

    def test(self, data):
        self.put(self.bulbs, data)


if __name__== "__main__":
    l = Hue()
    l.partyMode()
    # m = MusicPlayer()
    # m.romanticMode()
    # m.partyMode()
    # m.relaxingMode()

    # d = TrumpTweets()
    # d.readTweet()
