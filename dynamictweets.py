from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import Cursor



## this program gets real time tweets

class listener(StreamListener):

        def on_status(self, status):
                 print status.text.encode('utf-8')
                 #return True

#	def on_data(self, data):
#		print data

        def on_error(self, status):
                print('i got upto here')


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.userstream(track = ["#iraq"])
