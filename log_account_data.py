import csv
import tweepy
import pprint
from decouple import config
from datetime import date

pp = pprint.PrettyPrinter(indent=4)


# env variables
twitterKey = config("TWITTER_KEY")
twitterSecretKey = config("TWITTER_SECRET_KEY")
twitterToken = config("TWITTER_TOKEN")
twitterAccessToken = config("TWITTER_ACCESS_TOKEN")
twitterAccessTokenSecret = config("TWITTER_ACCESS_TOKEN_SECRET")

# authentication for Twitter API
auth = tweepy.OAuthHandler(twitterKey, twitterSecretKey)
auth.set_access_token(twitterAccessToken, twitterAccessTokenSecret)
api = tweepy.API(auth)

# retreive profile information
profile = api.me()._json
favourite_count = profile['favourites_count']
followers_count = profile['followers_count']
following_count = profile['friends_count']
tweet_count = profile['statuses_count']
current_date = date.today()

# write data to csv file
print('Writing data to CSV file...')
with open('data/account_data.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([current_date, favourite_count, followers_count, following_count, tweet_count])
print('Process completed.')
