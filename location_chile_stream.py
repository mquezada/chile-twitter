from streamer import *
from settings import *
import utils


#### 1 location in Chile
def stream_loc(api):
    for tweet in api.GetStreamSample():
        if not ('user' in tweet and 'location' in tweet['user'] and tweet['user']['location']):
            continue

        if utils.is_in_chile(tweet['user']['location']):
            print_tweet(tweet)
            yield tweet

api_loc = load_api('location-chile')
streamer_loc = stream_loc(api_loc)
save_tweets(streamer_loc, 'location-chile')