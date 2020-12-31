import json
import os
import random
import requests
import tweepy
from decouple import config
from bs4 import BeautifulSoup


# env variables
rapidAPIKey = config("RAPID_API_KEY")
twitterKey = config("TWITTER_KEY")
twitterSecretKey = config("TWITTER_SECRET_KEY")
twitterToken = config("TWITTER_TOKEN")
twitterAccessToken = config("TWITTER_ACCESS_TOKEN")
twitterAccessTokenSecret = config("TWITTER_ACCESS_TOKEN_SECRET")

def main():

    checks = False
    post = ""

    while checks == False:

        # get random word from RapidAPI's word API
        word, definition, part_of_speech = getRandomWord()

        # get the Italian translation of the word
        translation, ex_en, ex_it = scrapeForTranslation(word)
            
        # check to see the translation was successful
        if translation and ex_en and ex_it:

            # compile post and check length
            post = compilePost(word, translation, definition, part_of_speech)

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
    """
    Uses an API to get a random word.
    """

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

def scrapeForTranslation(word):
    """
    Takes in a word then scrapes Glosbe.com in order to get the Italian translation.
    If the word is not found the function returns none. 
    """
    # get the html from glosbe and make it soup
    source = requests.get(f'https://glosbe.com/en/it/{word}')
    soup = BeautifulSoup(source.text, features='html.parser')

    # check to see if there was an error finding the word
    possible_error = soup.find_all(class_='alert')

    if possible_error:
        print('Word not on Glosbe.')
        return None, None, None

    else:
        print('Word successfully pulled from Glosbe.')
        # pull out italian translation of word
        try:
            translated_word = soup.find(class_='phr').text
        except:
            translated_word = None

        # pull out example in english
        try:
            example_en = soup.find(class_='span6').text
        except:
            example_en = None

        # pull out the example in italian
        try:
            example_it = soup.find_all(class_='span6')[1].text
        except:
            example_it = None

        return translated_word, example_en, example_it

def formatText(input_text, formatting):
    """
    A function for formatting text to either italic or bold.
    """

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
    """
    Randomly selects three relevant hashtags.
    """

    hashtags = [
        "learnitalian", "italian", "learnlanguages", "vocabulary", "italiano", "wordaday", "dictionary", "languagelearning", "polyglot",
        "multilingual", "studyhard", "italy", "italiano", "bilingual", "dailyword", "wordaday"
    ]

    # get random ints
    random_ints = random.sample(range(len(hashtags)), 3)

    return hashtags[random_ints[0]], hashtags[random_ints[1]], hashtags[random_ints[2]]

def compilePost(word, translation, definition, part_of_speech):
    """
    Formats the contents of the post and makes sure the length is under 280 chars.
    """
    # get hashtags
    hash1, hash2, hash3 = getHashtags()

    # format text for examples
    word_bold = formatText(word.upper(), 'bold')
    trans_bold = formatText(translation.upper(), 'bold')
    arrow = formatText('=>', 'bold')

    # construct the tweet
    tweet = f"{trans_bold}\n\n{word.capitalize()}: {definition.capitalize()}.\n\n#{word.replace(' ', '')} #{hash1} #{hash2} #{hash3} "

    # check to be sure the length of the post is in limits
    if len(tweet) > 270:
        print("Post too long. Finding new word...")
        return None
    else:
        print("Post compiled successfully.")
        return tweet

def postTweet(post):
    """
    Sends the post to Twitter.
    """

    # authentication for Twitter API
    auth = tweepy.OAuthHandler(twitterKey, twitterSecretKey)
    auth.set_access_token(twitterAccessToken, twitterAccessTokenSecret)
    api = tweepy.API(auth)

    # update status, remove spaces from the word
    api.update_status(post)

    print("Post sent to Twitter.")

if __name__ == "__main__":
    main()