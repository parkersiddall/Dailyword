# Dailyword Twitter Bot
A script that automates the creation and posting of tweets which provide followers with a daily word in English and Italian. 

https://twitter.com/DailyWord_IT


## How it works

1. The script fetches a word and its definition from the Words API. 
2. The script scrapes the relevant page of WordReference.com in order to get the Italian translation of the word along with some example sentences in English and Italian.
3. The script runs a function that compiles and formats the text of the post, throwing some hashtags which are chosen at random from a list. Before the function returns the text of the post it checks to be sure it is within twitters 280 char limit. 
4. The script repeats these steps until there is a successful post compiled. 
5. In this script there is a line that requires users to 'confirm' the tweet before posting it. However this line is removed from the script that runs autonomously.  
6. The script sends the post off to Twitter using the Tweepy library. If the human does not confirm the post then the program quits. 






