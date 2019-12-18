from streamer import *
from settings import *
import datetime

api = load_api('news-seeds')
searcher = load_api('news-search', app=True)

def streamer_news(api, track):
    for tweet in api.GetStreamFilter(track=track, languages=LANGUAGES):
        print_tweet(tweet)
        yield tweet


while True:
    texts, keywords = timeline(api, MAINSTREAM_NEWS)
    track = prepare(keywords, NUM_KEYWORDS)

    to_search = [list(k) for k, _ in keywords[:NUM_KEYWORDS]]

    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    save_desc([' '.join(k) for k in to_search], 'current-news', f'{ts}_news_keywords')

    tweets = twitter_search(searcher, to_search)

    streamer = streamer_news(api, track)
    save_buffer(tweets, 'current-news', '_news_search')
    save_tweets(streamer=streamer, path='current-news', filename_suffix='_news_stream', stop_at_x_minutes=5)
