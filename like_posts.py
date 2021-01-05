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
            # language learning
            "learn italian",
            "learn languages",
            "italian",
            "italiano",
            "language learning",
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
            "translator",
            "language services",

            # Italy and geography
            "italy",
            "milan",
            "rome",
            "naples",
            "venice",
            "cinque terre",
            "turin",
            "bologna",
            "florence",
            "little italy",
            "mulberry street"

            # travel
            "travel",
            "wonderlust",
            "eurotrip",
            "trip to italy",
            "vacation",
            "mediterranean",
            "honeymoon",

            # study and university
            "semester abroad",
            "study in italy",
            "exchange student",
            "italian student",
            "unimi",
            "unibo",
            "bocconi",
            "bicocca",
            "american university of rome",
            "AUR",
            "JCU",
            "John Cabot University",
            "italian class",
            "IB",
            "International Baccalaureate",

            # italian food
            "pizza",
            "pasta",
            "carbonara",
            "spaghetti",
            "italian food",
            "italian cuisine",
            "parmesian cheese",
            "mozzarella",
            "wine",
            "prosecco",

            # italian sights
            "colosseum",
            "last supper",
            "sistine chapel",
            "the vatican",
            "the pantheon",
            "trevi fountain",
            "ponte vecchio"

            ]

# set some counters
new_likes = 0
already_liked = 0
result_limit = 150  # variable sets the count determining how many results each query will retreive

# make API calls and process results
for query in queries:

    print(f'Currently searching: {query}...')

    # retreive tweets for a specific hashtag
    learnItalian = api.search(q=query, count=result_limit)  #TODO add in language restriction

    for tweet in learnItalian:
        try:
            api.create_favorite(tweet.id)
            print(f'{tweet.id} liked.')
            new_likes += 1
        except:  #TODO create exceptions for specific errors
            print(f'{tweet.id} already liked or other error.')
            already_liked += 1

print(f'Process complete.\nNew likes: {new_likes}\nAlready liked: {already_liked}')

# log data
current_date = date.today()
num_queries = len(queries)
tot_queries_made = new_likes + already_liked

print('Writing data to CSV file...')
with open('data/like_posts_data.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([current_date, num_queries, result_limit, new_likes, already_liked, tot_queries_made])
print('Process completed.')



