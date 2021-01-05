import csv
import tweepy
from decouple import config
from datetime import date

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

# list out relevant hashtags to target anyone who may be interested in learning Italian
queries = [
    'learn italian', 
    'study in italy', 
    'italian class', 
    'italian vocabulary', 
    'italian words', 
    'italian language'
]

# track outcome
new_follows = 0
already_following = 0
result_limit = 10

for query in queries:

    print(f'Now searching recent tweets for {query}...')

    # search tweets to find people who want to learn italian
    learnItalian = api.search(q=query, count=result_limit, result_type='recent')

    # loop through results and like the follower of each tweet
    for tweet in learnItalian:

        # follow the user of the tweet
        try:
            api.create_friendship(id=tweet._json['user']['id'])
            print('New user followed.')
            new_follows += 1
        except:
            print('User already followed or other error.')
            already_following += 1

print(f'New follows: {new_follows}')
print(f'Already following: {already_following}')

# log data
current_date = date.today()
num_queries = len(queries)
tot_queries_made = new_follows + already_following

print('Writing data to CSV file...')
with open('data/follow_users_data.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([current_date, num_queries, result_limit, new_follows, already_following, tot_queries_made])
print('Process completed.')

