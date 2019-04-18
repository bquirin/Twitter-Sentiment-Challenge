import numpy as np
import matplotlib.pyplot as plt
import tweepy
import csv
from textblob import TextBlob

# Authenticate using keys and tokens
consumer_key = 'ENTER CONSUMER KEY'
consumer_secret = 'ENTER CONSUMER SECRET KEY'
access_token = 'ENTER ACCESS KEY'
access_token_secret = 'ENTER ACCESS SECRET KEY'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Prepare query
primeMinister = 'Theresa May'
count = 100

# Function to label tweet +ve or -ve


def getLabel(analysis, threshold=0):
    if analysis.sentiment[0] > threshold:
        return 'Positive'
    else:
        return 'Negative'


# Query Twitter
public_tweets = api.search(primeMinister, count=100)

# Save tweets and sentiment to CSV file
with open('sentiment.csv', 'w') as new_file:
    new_file.write('tweet,sentiment_label \n')
    label_list = []
    for tweet in public_tweets:
        tweetMessage = tweet.text
        analysis = TextBlob(tweetMessage)
        label = getLabel(analysis)
        label_list.append(label)
        new_file.write('{}, {} \n'.format(tweetMessage, label))


# Create numpy arrays and count number of +ve/-ve sentiments
np_labels = np.array(label_list)
positive = np.count_nonzero(np_labels == 'Positive')
negative = np.count_nonzero(np_labels == 'Negative')
total = positive + negative

# Create Pie Chart
opinion = 'Postive', 'Negative'
slices = [positive, negative]
cols = ['c', 'r']
plt.title("Public Opinion of Theresa May")
plt.pie(slices, labels=opinion, colors=cols, autopct='%.0f')
plt.show()
