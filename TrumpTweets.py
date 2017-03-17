import time, json, os
import requests as req
from requests_oauthlib import OAuth1

class TrumpTweets:
    def __init__(self):
        self.tweet_count = 1
        self.tweet_numbers = ['First', 'Second', 'Third', 'Fourth', 'Fifth']
        self.trump_twitter_account = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=realDonaldTrump&count=2'

        # Twitter API authentication parameters
        url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
        app_key = 'RG8zK6eIAZjIRpE4CpyJnY5oL'
        app_secret = '7MYbeKM6wkvjOLAwhm8FcpWdL3eVsJ2Ie3u4UnQMFKxYA4KHAG'
        oauth_token = '747079994665467904-IZRFmklnNOzPeCaDIt9oR1JfyCyD7yL'
        oauth_token_secret = '2dANaCZ9PtU8ZeRO4NN75tjxCI9DiKw4SeOCqSDFFmNox'


        # Get authentication 1.0 request
        auth = OAuth1(app_key, app_secret, oauth_token, oauth_token_secret)
        req.get(url, auth=auth)


        # Get latest trump tweets
        self.response = req.get(self.trump_twitter_account, auth=auth)
        self.tweet = json.loads(self.response.text)

    def readTweet(self):

        os.system("say 'Good morning Marc, it is -7 degrees outside. What better way to start your day than with a tweet from Donald Trump himself, read by yours truely, Microsoft Sam.'")

        time.sleep(1)
        tweet_text = self.tweet[1]['text']
        if 'https' in tweet_text:
            image_location = tweet_text.find('https')
            tweet_text = tweet_text[:image_location]

        os.system("say " + tweet_text + ' tweet')

        time.sleep(1)

        # Conclude
        os.system("say 'Have a great day. Boom chacalaca boom chacalacalaca.'")


if __name__ == "__main__":
    t = TrumpTweets()
    t.readTweet()
