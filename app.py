'''
import for twitter module: tweepy
'''
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
'''
import for manage conversion string to json
'''
import ujson
'''
import for sys like print on standard output
'''
import sys

from pusher import Pusher

from config import prod



# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key=CONSUMER_KEY
consumer_secret=CONSUMER_SECRET
access_token=OAUTH_TOKEN
access_token_secret=OAUTH_TOKEN_SECRET

pusher = Pusher(
  app_id=PUSHER_APP_ID,
  key=PUSHER_KEY,
  secret=PUSHER_SECRET
)

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):
        try:
            j = ujson.loads(data)
            text = j[u'text']
            url = j[u'entities']['urls'][0]['expanded_url']
            username = j[u'user']['screen_name']
            profile_image = j[u'user']['profile_image_url']
            lang = j[u'user']['lang']
            followers = j[u'user']['followers_count']
            timezone = j[u'user']['time_zone']
            sys.stdout.write("New Periscope detected: "+url+' ---> '+text+'\n')
            sys.stdout.flush()
            if (text.startswith( 'LIVE on #Periscope:' )):
                pusher.trigger(u'test_channel', u'my_event', {u'text': text, 'url': url, 'username': username,'profile_image': profile_image, 'lang': lang, 'followers': followers, 'timezone': timezone})
                
        except Exception as e:
            #print("Error")
            #print(type(e))
            print(e)
            print('.')
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['#periscope'])
