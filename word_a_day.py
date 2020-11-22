import json
import os
import random
import requests
import tweepy


# env variables
rapidAPIKey = os.environ.get("RAPID_API_KEY")
twitterKey = os.environ.get("TWITTER_KEY")
twitterSecretKey = os.environ.get("TWITTER_SECRET_KEY")
twitterToken = os.environ.get("TWITTER_TOKEN")
twitterAccessToken = os.environ.get("TWITTER_ACCESS_TOKEN")
twitterAccessTokenSecret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

def main():

    checks = False
    post = ""

    while checks == False:

        # get random word from RapidAPI's word API
        word, definition, part_of_speech = getRandomWord()

        # get the Italian translation of the word
        translation = translateToItalian(word)
            
        # check to see the translation was successful
        if translation:

            # compile post and check length
            post = compilePost(word, translation, definition)

            if post:
                checks = True

        else:
            continue

    print(post)

    human_approval = input("Do you want to proceed with this post, 'yes' or 'no'?...")

    if human_approval == "yes":
        # post the tweet
        postTweet(post)

        print(f"Program completed. The word is '{word}'.")
    else:
        quit

def getRandomWord():

    # URL call to get a random word
    url = "https://wordsapiv1.p.rapidapi.com/words/"

    # headers for request
    headers = {
    'x-rapidapi-key': rapidAPIKey,
    'x-rapidapi-host': "wordsapiv1.p.rapidapi.com"
    }
    
    # parameters for request
    querystring = {"random":"true", 
                    "hasDetails":"similarTo",  # be sure I am getting a word that has a definition
                    "lettersMax": 10 # to avoid long words or sayings
                }

    r = requests.request("GET", url, headers=headers, params=querystring)

    # check status code before going forward
    if r.status_code == 200:  

        rj = r.json()  # pull out the json
        word = rj["word"]  # isolate the name
        definition = rj["results"][0]["definition"]  # isolate the definition
        part_of_speech = rj["results"][0]["partOfSpeech"]  # isolate the part of speech

        # print update and return word, definition
        print("Word obtained successfully.")
        return word, definition, part_of_speech

    else:
        print("Error getting random word. Trying again...")

def translateToItalian(text):

    # identify URL for request
    url = "https://translation19.p.rapidapi.com/v1/translation/text"

    # create object data, inserting the word into the payload
    payload = {
        "source": {
            "dialect":"en", 
            "text": f"{text}"
        },
        "target":{
            "dialect":"it"
        }
    }

    # convert to json
    payload_string = json.dumps(payload)

    # declare headers
    headers = {
        'content-type': "application/json",
        'x-rapidapi-key': rapidAPIKey,
        'x-rapidapi-host': "translation19.p.rapidapi.com"
        }

    # make request
    response = requests.request("POST", url, data=payload_string, headers=headers)
    
    # check to be sure response is OK
    if response.status_code == 200:

        i = response.json()  # convert to json

        # print ok and return translation
        if i["target"]["text"] is None:
            print("Not able to translate the definition. Finding new word...")
        else:
            print("Translation received successfully.")
        return i["target"]["text"]

    else:
        print("Error retreiving translation.")
        return None

def formatText(input_text, formatting):

    # list of chars with different formatting
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    bold_chars = "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵"
    italic_chars = "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻0123456789"

    # empty string to store formatted text
    output = ""

    for character in input_text:
        if character in chars:
            if formatting == "bold":
                output += bold_chars[chars.index(character)]
            elif formatting == "italic":
                output += italic_chars[chars.index(character)]
        else:
            output += character 

    return output

def getHashtags():

    hashtags = [
        "learnitalian", "italian", "learnlanguages", "vocabulary", "italiano", "wordaday", "dictionary", "languagelearning", "polyglot",
        "multilingual", "studyhard", "italy", "italiano", "bilingual", "dailyword", "wordaday"
    ]

    # get random ints
    random_ints = random.sample(range(len(hashtags)), 3)

    return hashtags[random_ints[0]], hashtags[random_ints[1]], hashtags[random_ints[2]]

def compilePost(word, translation, definition):

    # make the word bold, part of speech to italic
    bold_word = formatText(translation.upper(), "bold")

    word_def = f"{word.capitalize()}: {definition.capitalize()}"
    word_def_italic = formatText(word_def, "italic")

    # get hashtags
    hash1, hash2, hash3 = getHashtags()

    # construct the tweet
    tweet = f"{bold_word}\n\n{word_def_italic}. \n\n#{word.replace(' ', '')} #{hash1} #{hash2} #{hash3} "

    # check to be sure the length of the post is in limits
    if len(tweet) > 280:
        print("Post too long. Finding new word...")
        return None
    else:
        print("Post compiled successfully.")
        return tweet

def postTweet(post):

    # authentication for Twitter API
    auth = tweepy.OAuthHandler(twitterKey, twitterSecretKey)
    auth.set_access_token(twitterAccessToken, twitterAccessTokenSecret)
    api = tweepy.API(auth)

    # update status, remove spaces from the word
    api.update_status(post)

    print("Post sent to Twitter.")

if __name__ == "__main__":
    main()