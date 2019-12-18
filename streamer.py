from twitter_keys import twitter_keys
from settings import *
from twitter import Api
import utils
import orjson
import gzip
import datetime
from pathlib import Path
from detect_keywords import detect_keywords
import logging
import unidecode
from colorama import init as colorama_init
from colorama import Fore, Back, Style
from typing import List


logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(funcName)s : %(message)s', level=logging.INFO)

colorama_init()


def load_api(name, app=False):
    key = twitter_keys.get(name)
    if not key:
        raise
    api = Api(
        key['consumer-key'],
        key['consumer-secret'],
        key['access-token'],
        key['access-token-secret'],
        application_only_auth=app
    )
    return api


def save_tweets(streamer, path, filename_suffix='', stop_at_x_minutes=None):
    buffer = list()
    ids = set()
    t0 = datetime.datetime.utcnow()

    logging.info("Streaming tweets...")
    for tweet in streamer:
        tweet_id = tweet.get('id')
        if not tweet_id or tweet_id in ids:
            continue
        ids.add(tweet_id)
        buffer.append(tweet)

        if len(buffer) >= BUFFER_SIZE:
            logging.info(f"Buffer full: total {len(buffer)} tweets")
            save_buffer(buffer, path, filename_suffix)
            buffer = []

        if stop_at_x_minutes and  datetime.datetime.utcnow() - t0 > datetime.timedelta(minutes=stop_at_x_minutes):
            logging.info(f"Timeout: total {len(buffer)} tweets")
            save_buffer(buffer, path, filename_suffix)
            buffer = []
            break


def save_buffer(tweets, path, filename_suffix=''):
    today = datetime.date.today().strftime('%Y-%m-%d')
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    folder = Path(f'{path}/{today}/')
    if not folder.exists():
        folder.mkdir(parents=True)

    filename = folder / Path(f'{ts + filename_suffix}.txt.gz')
    logging.info(f'writing {len(tweets)} tweets in {filename}')
    with gzip.open(filename, 'wb') as g:
        for t in tweets:
            g.write(orjson.dumps(t) + b'\n')
    logging.info(f"done writing to {filename}")


def save_desc(keywords: List[str], path, name):
    today = datetime.date.today().strftime('%Y-%m-%d')
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    folder = Path(f'{path}/{today}/')
    if not folder.exists():
        folder.mkdir(parents=True)

    filename = (folder / Path(f'{name}.txt'))
    logging.info(f"saving keywords to {filename}")
    with filename.open('w') as f:
        for tt in keywords:
            f.write(tt + '\n')


def api_search(api, query, num_pages):
    results = []

    tmp = api.GetSearch(
        term=query,
        result_type='mixed',
        return_json=True,
        count=100
    )

    for _ in range(num_pages):
        md = tmp.get('search_metadata')
        if tmp.get('statuses'):
            results.extend(tmp['statuses'])
            tmp = {}
        if not md:
            break
        next_ = md.get('next_results')
        if next_:
            tmp = api.GetSearch(raw_query=next_[1:], return_json=True)
        else:
            break
    return results


def twitter_search(api, track, max_limit=450):
    # 450 requests total to use with app only auth api
    total = len(track)
    num_pages = int(max_limit / total)
    res = []

    for keywords in track:
        tweets = api_search(api, query=' '.join(keywords), num_pages=num_pages)
        logging.info(f'searching {keywords}: total {len(tweets)} tweets')
        res.extend(tweets)

    uniq_tweets = dict()
    for t in res:
        uniq_tweets[t['id']] = t
    logging.info(f'Total {len(uniq_tweets)} tweets')
    return list(uniq_tweets.values())


def user_tweets_last_hour(api, screen_name):
    now = datetime.datetime.now(datetime.timezone.utc)
    tweets = api.GetUserTimeline(
        screen_name=screen_name,
        count=200,
        include_rts=False,
        trim_user=True,
        exclude_replies=True
    )
    min_date = min([parse_twitter_date(t.created_at) for t in tweets])
    
    while now - min_date < datetime.timedelta(hours=1):
        min_id = min([t.id for t in tweets])
        more_tweets = api.GetUserTimeline(
            screen_name=screen_name,
            count=200,
            include_rts=False,
            trim_user=True,
            exclude_replies=True,
            max_id=min_id - 1
        )
        tweets.extend(more_tweets)
        min_date = min([parse_twitter_date(t.created_at) for t in tweets])

    return tweets

def parse_twitter_date(created_at):
    #  'Thu Dec 12 17:27:03 +0000 2019'
    dt = datetime.datetime.strptime(created_at, '%a %b %d %H:%M:%S %z %Y')
    return dt


def timeline(api, screen_names):
    logging.info("Gettings headlines from news accounts")
    tweets = []
    for screen_name in screen_names:
        tweets_ = user_tweets_last_hour(api, screen_name)
        tweets.extend(tweets_)
        logging.info(f"Timeline of @{screen_name}: {len(tweets_)} tweets")

    # remove duplicates
    logging.info(f"Total {len(tweets)} tweets. Tokenizing text...")
    texts = set([frozenset(utils.tokenize(t.text)) for t in tweets])
    # get keywords

    logging.info(f"Total {len(texts)} texts. Extracting keywords...")
    return texts, detect_keywords(texts)


def prepare(keywords_list, max_keywords=20):
    logging.info("generating keywords to stream")
    # [(frozenset({'acusación', 'constitucional', 'piñera'}), 7944), ...]
    MAX_KEYWORDS = 400  # https://developer.twitter.com/en/docs/tweets/filter-realtime/api-reference/post-statuses-filter
    track = []
    for keyword_set, _ in keywords_list[:max_keywords]:
        # buscar por las keywords encontradas
        orig_track = ' '.join(keyword_set)
        track.append(orig_track)
        # buscar por las keywords encontradas, sin tildes
        clean_track = ' '.join(unidecode.unidecode(word) for word in keyword_set)
        if orig_track != clean_track:
            track.append(clean_track)

    logging.info(f"total {len(track)} keyword sets")
    return track

def print_tweet(tweet, use_log=True):
    if 'text' in tweet:
        txt = ' '.join(tweet['text'].split())
        uname = f"{tweet['user']['name']}"
        uscreen = f"@{tweet['user']['screen_name']}"
        fmt =  Fore.BLUE + f"{uname} ({uscreen})" + Style.RESET_ALL
        fmt = fmt + f": {txt}"
        if use_log:
            logging.info(fmt)
        else:
            print(fmt)


# api = load_api('bounding-box', app=True)
# texts, keywords = get_keywords_from_accounts(api, MAINSTREAM_NEWS)
# track, _ = prepare_keywords_for_stream(keywords, 20)



# for tweet in api.GetStreamFilter(track=track):
#     print_tweet(tweet)


# for tweet in api.GetStreamFilter(locations=CHILE_BOUNDING_BOX, languages=LANGUAGES):
#      print(f"@{tweet['user']['screen_name']}: {' '.join(tweet['text'].split())}")
#      if ('user' in tweet and 'location' in tweet['user'] and tweet['user']['location']):
#          print('location:', tweet['user']['location'])
# for tweet in api.GetStreamSample():
#     #if not ('user' in tweet and 'description' in tweet['user'] and tweet['user']['description']):
#     #    continue
#     if not ('user' in tweet and 'location' in tweet['user'] and tweet['user']['location']):
#         continue
#     if utils.is_in_chile(tweet['user']['location']):
#         print(f"@{tweet['user']['screen_name']}: {' '.join(tweet['text'].split())}")
#         print('location:', tweet['user']['location'])
#         print()


# ####### 2 trending topics
# trending_topics = api.GetTrendsWoeid(woeid=CL_WOEID)
# trend_keywords = [tt.name for tt in trending_topics]
# for tweet in api.GetStreamFilter(track=trend_keywords, languages=LANGUAGES):
#     if 'user' not in tweet:
#         continue
#     print(f"@{tweet['user']['screen_name']}: {' '.join(tweet['text'].split())}")


# ####### 3 keywords
# for tweet in api.GetStreamFilter(track=TRACK_KEYWORDS, languages=LANGUAGES):
#     if 'user' not in tweet:
#         continue
#     print(f"@{tweet['user']['screen_name']}: {' '.join(tweet['text'].split())}")


###### 4 noticias



