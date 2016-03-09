import threading

import tweepy

access_token = "1281571783-BkkijSiyc7FFxXUmjqYUDzSq4eafSkFVujxDbsL"
access_token_secret = "LRgJk7HTtRMsPgp8QFzCkFra25BiCghqaP0S28mMdQxXw"
consumer_key = "mOxISQevRFV4qlUL2BJTL9pAv"
consumer_secret = "5MbnCpt8KZcGuev4gPdDROqw0QRyb6mpHR1fUWdbzDrsRlEIqB"


class KeywordListener(tweepy.StreamListener):
    """Twitter listener that performs statistical analysis
    on a the frequencies of a single twitter keyword.
    """
    def __init__(self, keyword, auth):
        super(KeywordListener, self).__init__()
        self.keyword = keyword
        self.stream = tweepy.Stream(auth, self)
        self.stream.filter(track=[self.keyword], async = True)

    def on_status(self, status):
        print(self.keyword)
        return True

    def on_error(self, status):
        print(status)

keywords = [
    "Bernie Sanders",
    "Hillary Clinton"
]

if __name__ == '__main__':
    listeners = []
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    for keyword in keywords:
        listeners.append(KeywordListener(keyword, auth))

