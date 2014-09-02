from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import Cursor


ckey = 'bA85nhCE0oNX2LAaWsCaDpXB5'
csecret = 'yme14hGPfh02Ltz1GHVVDIo901TD1kGOf6HREv6Yb92Q5J4axB'
atoken = '115818322-bVwit9ICJ2KDjDodDNWmpxuu6L1jqBwME7zgA08G'
asecret = 'MJeOtbjm2v4tduAWU4Z4zfQO1wUrCPZtrRjLVE9TJxAh4'

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
