from streamer import *
from settings import *

#### 0 bounding box
api_bb = load_api('bounding-box')

def stream_bb(api):
    for tweet in api_bb.GetStreamFilter(locations=CHILE_BOUNDING_BOX, languages=LANGUAGES):
        print_tweet(tweet)
        yield tweet

save_tweets(stream_bb(api_bb), 'bounding-box')
