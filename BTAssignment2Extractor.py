# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 12:19:25 2015

Description:

This script enables one with multiple twitter keys to cycle through them, and make repeated API
requests to extract the tweets of different users into CSV files.

@author: Thiru
"""

import time,tweepy,csv
#import accesstokenTwitter 

#Uncomment above if you have a config file with a lst
#of accesstokens, else, add manually below in the form of
# ClientID/ Client Secret/ Access Token / Access Secret

#Eg,

#accesstokenlist=[]
#accesstokenlist.append(['clientid','clientsecret','accesstoken','accesssecret'])

"""
PreCond: Takes in a lst of twitter screennames.

Description: Writes CSV's of the user's latest 3.2k tweets in utf-8 format.
            one CSV per user.

Instructions: If you want to start from a specific user, change startFrom from
              0 to the index of the user. Else, just run.
"""
def extractTweets(lst):
    currKeyID=0
    currentKey=accesstokenlist[currKeyID]
    startFrom=0  ##If Continuing from previous save, put start index here.
    numtoken=len(accesstokenlist)     # Total number of access keys
    auth = tweepy.auth.OAuthHandler(currentKey[0], currentKey[1])
    auth.set_access_token(currentKey[2], currentKey[3])
    api = tweepy.API(auth)
    skippedlist=[]
    rateID=0
    timeStart=time.time()
    
    def changekey():
        nonlocal currKeyID
        nonlocal currentKey
        nonlocal numtoken
        nonlocal api,auth
        currKeyID = (currKeyID+1)%numtoken
        currentKey=accesstokenlist[currKeyID]
        auth = tweepy.auth.OAuthHandler(currentKey[0], currentKey[1])
        auth.set_access_token(currentKey[2], currentKey[3])
        api = tweepy.API(auth)
        
    def updateAPIRate():
        nonlocal rateID
        x=api.rate_limit_status()
        rateID=x['resources']['statuses']['/statuses/user_timeline']['remaining']
        
    def checkRateID():
        nonlocal rateID
        nonlocal timeStart
        if rateID<=1:
            changekey()
            updateAPIRate()
            if rateID<=1:
                timeDifference = time.time() - timeStart
                if timeDifference > 0:
                    print('RateID Exhausted, sleeping for rate reset. Key: '+str(currKeyID)) 
                    time.sleep(905 - timeDifference)
                    timeStart = time.time()
                    
    for i in range(startFrom,len(lst)):
        try:
            print('Currently processing User: '+str(i))
            tweetlst = []
            new_tweets = api.user_timeline(screen_name = lst[i],count=200)
            tweetlst.extend(new_tweets)
            updateAPIRate()
            checkRateID()

            ##CURRENTLY SET TO 200 TWEETS PER USER. IF YOU WANT ALL, UNCOMMENT THE FOLLOWING.
#            oldest = tweetlst[-1].id - 1
#            while len(new_tweets) > 0:
#                checkRateID()
#                rateID-=1
#                new_tweets = api.user_timeline(screen_name = lst[i],count=200,max_id=oldest)
#                tweetlst.extend(new_tweets)
#                oldest = tweetlst[-1].id - 1
                
            outtweets = [[lst[i].screen_name,tweet.created_at,tweet.retweet_count,tweet.favorite_count, tweet.text.encode('utf8')] for tweet in tweetlst]
            		
            with open('%s_tweets.csv' % lst[i], 'w',newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["id","created_at","retweet count","favourite count","text"])
                writer.writerows(outtweets)
        
        except Exception as e:
            print(e, 'Error occured while processing user. Skipping!')
            print('Currently using key: '+str(currKeyID))
            skippedlist.append(i)
            print('Number of skipped users: '+ str(len(skippedlist)))
            print(skippedlist)
	
extractTweets(lst)
