import feedparser
import sys
import re
import OSC
from bs4 import BeautifulSoup
from pyphen import Pyphen
from time import sleep

# settings
TEXT_WIDTH = 80

# set up hypenator dictionary
hyph = Pyphen(lang='en_US')

# create OSC sender
client = OSC.OSCClient()
client.connect(('127.0.0.1', 6449))

def print_word(word):
    # cut out punctuation and digits
    alpha = re.sub('[^a-zA-Z]', '', word)

    if (alpha): # if word contains letters
        # calculate syllables in word
        syllables = len(hyph.inserted(alpha).split('-'))

        # send syllabes to ChucK via OSC
        msg = OSC.OSCMessage()
        msg.setAddress('/demo/rhythm/subdiv')
        msg.append(syllables)
        client.send(msg)

        # print word
        print(word),
        sys.stdout.flush()
        
        # space out
        # NOTE: should definitely take timing information from
        # ChucK if possible
        sleep(0.5)
    else: # word didn't have any letters, so just print for clarity of output
        print(word),
        
def print_string(string):
    line_chars = 0
    words = string.split(' ')

    for word in words:
        print_word(word)

        # wrap text
        line_chars += len(word) + 1
        if (line_chars > TEXT_WIDTH) and word != words[-1]:
            print
            line_chars = 0

    print

def analyze_feed(url):
    feed = feedparser.parse(url)
    print('\n\t' + feed.feed.title + '\n')
    for entry in feed.entries:
        # print title
        print_string(entry.title)
        print('-' * len(entry.title))

        # print body
        text = BeautifulSoup(entry.content[0].value, 'html.parser').get_text()
        print_string(text)
        print

# NPR News
analyze_feed('http://www.npr.org/rss/rss.php?id=1001')
