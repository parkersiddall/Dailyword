import tweepy
from decouple import config


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
hashtags = [
            # language learning
            "learnitalian",
            "learnlanguages", 
            "italian", 
            "italiano",
            "languagelearning",
            "polyglot",
            "multilingual", 
            "bilingual", 
            "duolingo", 
            "rosetta stone", 
            "babel", 
            "linguist", 
            "linguistics", 
            "translate", 
            "translation",
 
            # Italy and geography
            "italy", 

            # travel
            "travel", 
            "wonderlust", 
            "eurotrip", 
            
            # study abroad
            "semester abroad", 
            "study abroad"
            ]

# set some counters
new_likes = 0
already_liked = 0

for hashtag in hashtags:

    print(f'Currently searching: {hashtag}...')

    # retreive tweets for a specific hashtag
    learnItalian = api.search(q=hashtag, count=25)  #TODO add in language restriction

    for tweet in learnItalian:
        try:
            api.create_favorite(tweet.id)
            print(f'{tweet.id} liked.')
            new_likes += 1
        except:
            print(f'{tweet.id} already liked.')
            already_liked += 1

print(f'Process complete.\nNew likes: {new_likes}\nAlready liked: {already_liked}')