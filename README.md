# Twitter-Tweetxractor

This script enables one with multiple twitter keys to cycle through them, and make repeated API
requests to extract the tweets of different users into CSV files. 

Instructions:

1) Have an accesstokenlist.py file containing a list called accesstokenlist with all your twitter API keys appended in the form of
ClientID/ClientSecret/Accesstoken/Access secret

OR

2) Manually add into the script yourself.

input a list of screen-names of users that you want to extract, and it'll create a CSV file with the tweets of each user.

**Default set to take latest 200 tweets only. If you want all 3.2k tweets, uncomment the commented part.
