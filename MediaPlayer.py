import vlc, time
class MediaPlayer:
    def __init__(self):
        self.VlcInstance = vlc.Instance()
        self.player = self.VlcInstance.media_player_new()

        self.romanticMusic = self.VlcInstance.media_new('./Music/Yello - Oh Yeah.flac')
        self.partyMusic = self.VlcInstance.media_new('./Music/Haddaway - What Is Love4.flac')

    def romanticMode(self):
        self.player.set_media(self.romanticMusic)

        self.player.play()
        time.sleep(15)

    def partyMode(self):
        self.player.set_media(self.partyMusic)

        self.player.play()
        time.sleep(15)

    def morningMode(self):
        d = TrumpTweets()
        d.readTweet()


if __name__ == "__main__":
    m = MediaPlayer()
    m.partyMode()

