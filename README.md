# DailyWord Twitter Bot
A series of scripts that automates the creation and posting of daily tweets, each containing an Italian word and its translation to English. Interaction with other tweets and users is also automized and runs on an hourly basis.

https://twitter.com/DailyWord_IT


## word_a_day.py
- The script fetches a word and its definition from the Words API. 
-  The script scrapes the relevant page of Glosbe.com in order to get the Italian translation of the word along with some example sentences in English and Italian.
-  The script runs a function that compiles and formats the text of the post, throwing some hashtags which are chosen at random from a list. Before the function returns the text of the post it checks to be sure it is within twitters 280 char limit. 
-  The script repeats these steps until there is a successful post compiled. 
-  In this script there is a line that requires users to 'confirm' the tweet before posting it. However this line is removed from the script that runs autonomously.  
-  The script sends the post off to Twitter using the Tweepy library. If the human does not confirm the post then the program quits. 


## like_posts.py
- The script loops through a list of terms that would be relevant to someone hoping to learn Italian. With each loops it searches Twitter posts and returns 25 tweets that should be relevant to the term. 
- The script then loops through each tweet that is return and sends and API call to add the tweet to favorites. If the tweet has already been liked then it moves on to the next tweet. 
- Counters are kept so that I can check the logs to see how easily check how effective the script is. 


## follow_users.py
- The script loops through a list of relevent terms or phrases that would be relevent to someone interested in learning Italian (NOTE: terms are not identical to the ones used to like posts, they are narrower) and returns a tweets that match. 
- For each tweet returned, the script extracts the posters ID then makes an API call to follow that user. If the user is already followed then the script moves to the next tweet. 
- Counters are kept so that I can check the logs and easily see how effective the script is. 


The scripts are all run on a schedule through pythonanywhere.com. Posts are created once per day, likes and follows are done hourly.







