from streamer import *
from settings import *
from pathlib import Path
import datetime
import orjson
import gzip


####### 2 trending topics
api_tt = load_api('trending-topics')
searcher = load_api('tt-search', app=True)

def streamer_tt(api, track):
    for tweet in api.GetStreamFilter(track=track, languages=LANGUAGES):
        print_tweet(tweet)
        yield tweet


while True:
    buffer = []
    trending_topics = api_tt.GetTrendsWoeid(woeid=CL_WOEID)
    trend_keywords = [tt.name for tt in trending_topics]
    tweets = twitter_search(searcher, trend_keywords)
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    save_desc(trend_keywords, 'trending-topics', f'{ts}_trending_topics')
    streamer = streamer_tt(api_tt, trend_keywords)
    save_buffer(tweets, 'trending-topics', '_tt_search')
    save_tweets(streamer, 'trending-topics', MINUTES_TT)

