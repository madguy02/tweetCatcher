from os import environ
import tweepy
import sys
import getopt

from env_config import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET

class Authentication:
    def __init__(self) -> None:
        self.consumer_key = f"{environ.get(CONSUMER_KEY)}"
        self.consumer_secret = f"{environ.get(CONSUMER_SECRET)}"
        self.access_token = f"{environ.get(ACCESS_TOKEN)}"
        self.access_token_secret = f"{environ.get(ACCESS_TOKEN_SECRET)}"
    
    def instantiate_auth(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)

        return auth

class Tweet_Scrapper:

    def __init__(self, username) -> None:
        self.username = username
    
    def retrieve_tweets(self):
        auth = Authentication()
        inst_auth = auth.instantiate_auth()
        api = tweepy.API(inst_auth)

        tweets = []

        for twt in tweepy.Cursor(api.user_timeline, screen_name=self.username, tweet_mode = 'extended').items():
            tweets.append(twt)

        return tweets
    
    def format_tweets(self):
        tweets = self.retrieve_tweets()
        tweet_list = []
        for tweet in tweets:
            tweet_list.append(tweet.full_text)
        
        return tweet_list

class Tweet_Saver:
    def __init__(self, tweet_list, username) -> None:
        self.tweet_list = tweet_list
        self.username = username
    
    def save_tweets_text(self):
        with open(f"{self.username}.txt", "a") as f:
            for line in self.tweet_list:
                f.write(line)
                f.write("\n\n")
                f.write("------------")
                f.write("\n")
        
        print("Tweets saved!!")
        f.close()




if __name__ == "__main__":

    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "u:h:")
    except:
        raise ValueError('provided argument not supported')
    
    for opt,arg in opts:

        if opt in ['-u']:
            tweet_scrapper = Tweet_Scrapper(arg)
            tweets = tweet_scrapper.format_tweets()

            tweet_saver = Tweet_Saver(tweets, arg)
            tweet_saver.save_tweets_text()

        elif opt in ['-h']:
            print('''
            -u: get all tweets for a user
            -h: help
            '''
            )

    
