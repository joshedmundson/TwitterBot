import tweepy as tp 
import logging 

class TwitterBot(tp.API):
    '''
    A class to extend the functionality of the tweepy.API class.
    '''
    def __init__(self, consumer_key, consumer_secret, access_token, access_secret, *, 
                 cache=None, host='api.twitter.com', parser=None, proxy=None, retry_count=0, 
                 retry_delay=0, retry_errors=None, timeout=60, upload_host='upload.twitter.com', 
                 user_agent=None, wait_on_rate_limit=False):
        super().__init__(self, cache=None, host='api.twitter.com', parser=None, proxy=None, 
                         retry_count=0, retry_delay=0, retry_errors=None, timeout=60, 
                         upload_host='upload.twitter.com', user_agent=None, 
                         wait_on_rate_limit=False)
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_secret = access_secret 
        # Automatically authenticate Twitter credentials when instanciated
        self.auth = self.generate_auth(self.consumer_key, self.consumer_secret, 
                                      self.access_token, self.access_secret)
        # Configure the format of the data log to include the date and time
        logging.basicConfig(filename='bot.log', filemode='w', format='%(asctime)s - %(message)s', 
                            level=logging.INFO)
        # Make sure the the credentials are actually real and log any errors
        self.me = self.verify_auth_keys()


    def generate_auth(self, consumer_key, consumer_secret, access_token, access_secret):
        '''Method that generates and returns an auth connection to twitter'''
        auth = tp.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        return auth
    
    
    def verify_auth_keys(self):
        '''Method that verifies the credientials used to create the auth connection'''
        try:
            me = self.verify_credentials()
            logging.info("Credentials Verified")
            print('Credentials Verified')
            return me
        except Exception as e:
            logging.error("Failed to Verify Credentials", exc_info=True)
            print(f"Failed to Verify Credentials:\n{e}")
            
            
    def get_latest_tweet(self, user_name=None, user_id=None):
        '''Method that fetches the latest tweet from the passed user'''
        if user_name:
            user = self.get_user(screen_name=user_name)
            latest_tweet = self.user_timeline(id=user.id)[0]
            return latest_tweet
        if user_id:
            latest_tweet = self.user_timeline(id=user_id)[0]
            return latest_tweet
        
    
    def get_replies(self, tweet):
        '''Method returns a list of tweeted replies to the passed tweet'''
        original_user = tweet.user
        original_user_screen_name = original_user.screen_name
        responses_to_original_user = self.search_tweets(q="to:"+original_user_screen_name)
        responses_to_original_tweet = []
        for response in responses_to_original_user:
            if response.in_reply_to_status_id == tweet.id:
                responses_to_original_tweet.append(response)
        return responses_to_original_tweet
    
    
    def previously_commented_on_tweet(self, tweet):
        '''Method that checks if the active user previously commented on the passed tweet'''
        tweet_comments = self.get_replies(tweet)
        tweet_comment_ids = [comment.user.id for comment in tweet_comments]
        if self.me.id in tweet_comment_ids:
            return True 
        else:
            return False 
