import tweepy
import datetime as DT
from time import sleep

from app import db, Handle, HandleData

consumer_key = 'zg9yQTGTT2oizk3XLMHGLzfpJ'
consumer_secret = 'nmiwqRpWDX0oxTCUTro8sPeUVUXIZHW9O1VZcTb0mLyfHw51sc'
access_token = '700001043-oxm3LZ72y4WmWGRqY66QjV0SzZoHGy5OGgwic26M'
access_token_secret = 'hGJZWTb5bjGFSiuIQrff5UajKdlyXcp7Lyun5SJzq05Su'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def getRetweets(name):
    user = api.get_user(name)
    tweets = api.user_timeline(user.id, count=200, include_rts=False)

    retweet_sum = 0
    for tweet in tweets:
    	retweet_sum += tweet.retweet_count
   	#loop through each tweet and add to sum
    return retweet_sum

def write_to_db():
    handles = Handle.query.all()

    total_retweets = 0
    r = []
    for handle in handles:
        retweets = getRetweets(handle.name)#get the retweets
        r.append(retweets)#add to a list for further analysis

        handledata = HandleData(retweets=retweets, handle=handle.id, timestamp = DT.datetime.now())#add to database
        db.session.add(handledata)
        db.session.commit()
        total_retweets += r[-1]#get the most recently added tweet
        print handle.name, retweets

    average_retweets = total_retweets / float(len(handles))

    i = 0
    while i<len(handles):
        cost = ((r[i]/average_retweets) * 100) / 5
        person = Handle.query.filter_by(name=handles[i]).first()
        person.cost = cost
        db.session.commit()
        i+=1

    return True
    
if __name__=="__main__":
    write_to_db()
    #last_week = DT.datetime.today() - DT.timedelta(days=1)
    #print getRetweets("realDonaldTrump", last_week, 7)