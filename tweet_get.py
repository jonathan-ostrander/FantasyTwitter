import tweepy
import datetime as DT

consumer_key = 'asdf'
consumer_secret = 'sdf'
access_token = 'asdf'
access_token_secret = 'asdf'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def getRetweets(name, begin, delta):
    after = begin + DT.timedelta(days=delta['days'],
                               hours=delta['hours'],
                               minutes=delta['minutes'])
    user = api.get_user(name)
    #tweets = api.user_timeline(user.id, count=200, include_rts=False)
    tweets = tweepy.Cursor(api.user_timeline, count=200).pages(16)

    retweet_sum = 0
    '''
    i=0
    while i < len(tweets):
        if after > tweets[i].created_at > begin:
            retweet_sum += tweets[i].retweet_count
        i+=1
    '''

    for tweet in tweets:
    	if after > tweet.created_at > begin:
    		retweet_sum += tweet.retweet_count
   	#loop through each tweet and add to sum
    
    while tweets[-1].created_at > begin:
        #tweets = api.user_timeline(user.id, max_id=tweets[-1].id, count=200, include_rts=False)
        tweets = tweepy.Cursor(api.user_timeline, count=200).pages(16)
        for tweet in tweets:
	    	if after > tweet.created_at > begin:
	    		retweet_sum += tweet.retweet_count
	    #loop through and add each tweet to su
    return retweet_sum
    
if __name__=="__main__":
    pass
    #last_week = DT.datetime.today() - DT.timedelta(days=1)
    #print getRetweets("realDonaldTrump", last_week, 7)