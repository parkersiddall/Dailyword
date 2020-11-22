# Dailyword Twitter Bot
A script that automates the posting of a daily Italian word and its English counterpart to Twitter using various APIs.

https://twitter.com/Dailyword_EN_IT

***Note***: *The translation API that I use is not very good, in most cases the translations are off. For now the script requires human approval before sending the post off to Twitter. Once I find a more reliable translation API I will set this script up to run automatically as a cronjob.*

## How it works

1. The script fetches a word and its definition from the Words API. 
2. The script sends the word off to be translated to Italian via the iTranslate API (not great).
3. The script runs a function that compiles and formats the text of the post, throwing some hashtags which are chosen at random from a list. Before the function returns the text of the post it checks to be sure it is within twitters 280 char limit. 
4. The script repeats these steps until there is a successful post compiled. 
5. Then the script awaits user input to confirm that the translation/post makes sense. 
6. After given confirmation the script sends the post off to Twitter using the Tweepy library. If the human does not confirm the post then the program quits. 






