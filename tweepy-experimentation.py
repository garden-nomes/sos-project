import threading
import time
import sys
import json

from numpy import mean, std, interp
import tweepy

access_token = "1281571783-BkkijSiyc7FFxXUmjqYUDzSq4eafSkFVujxDbsL"
access_token_secret = "LRgJk7HTtRMsPgp8QFzCkFra25BiCghqaP0S28mMdQxXw"
consumer_key = "mOxISQevRFV4qlUL2BJTL9pAv"
consumer_secret = "5MbnCpt8KZcGuev4gPdDROqw0QRyb6mpHR1fUWdbzDrsRlEIqB"

BIG_WINDOW = 1000
LITTLE_WINDOW = 20

class KeywordListener(tweepy.StreamListener):
    """Twitter listener that performs statistical analysis
    on a the frequencies of a single twitter keyword.
    """
    def __init__(self, keyword, auth):
        # call StreamListener init
        super(KeywordListener, self).__init__()

        # set up fields
        self.keyword = keyword
        self.last_hit = None
        self.hits = []

        # start listener
        self.stream = tweepy.Stream(auth, self)
        self.stream.filter(track=[self.keyword], async = True)

    def on_status(self, status):
        current_time = time.clock()
        if self.last_hit == None:
            # this is the first hit
            self.last_hit = current_time
        else:
            # record the interval between hits
            self.hits.append(current_time - self.last_hit)
            self.last_hit = current_time

            # cap hits length
            if len(self.hits) > BIG_WINDOW:
                self.hits = self.hits[-BIG_WINDOW:]

            if len(self.hits) > LITTLE_WINDOW:
                stdDev = std(self.hits)
                avg = mean(self.hits)
                lower = avg - 2 * stdDev
                upper = avg + 2 * stdDev
                print(interp(mean(self.hits[-LITTLE_WINDOW:]), [lower, upper], [0, 1]))


        return True

    def on_error(self, status):
        print(status)
        self.stream.disconnect()

keywords = [
    "Bernie Sanders",
]

if __name__ == '__main__':
    listeners = []
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # for arg in sys.argv[1:]:
        # print("Creating listener for %s..." % arg)
        # listeners.append(KeywordListener(arg, auth))
    for keyword in keywords:
        listeners.append(KeywordListener(keyword, auth))

