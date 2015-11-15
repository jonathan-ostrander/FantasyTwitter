import tweepy
import datetime as DT

consumer_key = 'asdaasd'
consumer_secret = 'asd'
access_token = '700001043-asd'
access_token_secret = 'asf'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def getRetweets(name, begin, delta):
    after = begin + DT.timedelta(days=delta)
    user = api.get_user(name)
    tweets = api.user_timeline(user.id, count=200, include_rts=False)
   
    print "date", tweets[-1].created_at

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
        tweets = api.user_timeline(user.id, max_id=tweets[-1].id, count=200, include_rts=False)
        for tweet in tweets:
	    	if after > tweet.created_at > begin:
	    		retweet_sum += tweet.retweet_count
	    #loop through and add each tweet to su
    return retweet_sum
    
if __name__=="__main__":
    last_week = DT.datetime.today() - DT.timedelta(days=1)
    print getRetweets("realDonaldTrump", last_week, 7)