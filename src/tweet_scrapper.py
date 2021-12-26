# TODO: Refactor the classes and methods
from os import environ
import tweepy
import sys
import getopt

from env_config import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET

class Authentication:
    def __init__(self) -> None:
        self.consumer_key = environ.get("CONSUMER_KEY")
        self.consumer_secret = environ.get("CONSUMER_SECRET")
        self.access_token = environ.get("ACCESS_TOKEN")
        self.access_token_secret = environ.get("ACCESS_TOKEN_SECRET")
    
    def instantiate_auth(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)

        return auth

class Tweet_Scrapper:

    def __init__(self, username, api) -> None:
        self.username = username
        self.api = api
    
    def retrieve_tweets(self):

        tweets = []

        for twt in tweepy.Cursor(self.api.user_timeline, screen_name=self.username, tweet_mode = 'extended').items():
            tweets.append(twt)

        return tweets
    
    def format_tweets(self):
        tweets = self.retrieve_tweets()
        tweet_list = []
        for tweet in tweets:
            tweet_list.append(tweet.full_text)
        
        return tweet_list

class Tweet_Saver:
    def __init__(self, username) -> None:
        self.username = username
    
    def save_tweets_text(self, tweet_list):
        with open(f"{self.username}.txt", "a") as f:
            for line in tweet_list:
                f.write(line)
                f.write("\n\n")
                f.write("------------")
                f.write("\n")
        
        print("Tweets saved!!")
        f.close()
    
    def save_followers_text(self, followers):
        with open(f"{self.username}_followers.txt", "a") as f:
            for follower in followers:
                f.write(follower)
                f.write("\n\n")
                f.write("------------")
                f.write("\n")
        
        print("Followers saved!!")
        f.close()


class Followers_List:
    def __init__(self, username, api) -> None:
        self.username = username
        self.api = api

    def get_followers(self):
        followers_list = []
        for follower in self.api.get_followers(screen_name = self.username):
            followers_list.append(follower.name)
        
        return followers_list

if __name__ == "__main__":

    argv = sys.argv[1:]

    auth = Authentication()
    inst_auth = auth.instantiate_auth()
    api = tweepy.API(inst_auth)


    try:
        opts, args = getopt.getopt(argv, "u:h:f:")
    except:
        raise ValueError('provided argument not supported')
    
    for opt,arg in opts:

        if opt in ['-u']:
            
            tweet_scrapper = Tweet_Scrapper(arg, api)
            tweets = tweet_scrapper.format_tweets()

            tweet_saver = Tweet_Saver(arg)
            tweet_saver.save_tweets_text(tweets)

        elif opt in ['-h']:
            print('''
            -u: get all tweets for a user
            -h: help
            '''
            )
        elif opt in ['-f']:
           followers =  Followers_List(arg, api)
           list = followers.get_followers()
           tweet_saver_followers = Tweet_Saver(arg)
           tweet_saver_followers.save_followers_text(list)
        
        else:
            print('Sorry not yet supported!!')




    
