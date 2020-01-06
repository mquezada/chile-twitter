from pathlib import Path
import datetime
import orjson
from db import schema, models, db_manager
from tqdm import tqdm

import gzip
from sqlalchemy.orm import sessionmaker
import logging

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(funcName)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


Session = sessionmaker(bind=db_manager.engine)
tweet_sc = schema.Tweet()
user_sc = schema.User()


def save_file(path, file_, source_id, source_type='stream'):
    session = Session()
    tweet_batch = []
    user_batch = []
    logger.info(f"Loading json file {path}")
    for line in file_:
        tweet_obj = orjson.loads(line)

        if tweet_obj['is_quote_status']:
            q = tweet_obj.get('quoted_status')
            if q:
                u = q['user']
                q['user_id'] = u['id']
                q['source_type'] = source_type
                q['source_id'] = source_id
                tweet_batch.append(q)
                user_batch.append(u)

        elif 'retweeted_status' in tweet_obj:
            rt = tweet_obj.get('retweeted_status')
            if rt:
                u = rt['user']
                rt['user_id'] = u['id']
                rt['source_type'] = source_type
                rt['source_id'] = source_id
                tweet_batch.append(rt)
                user_batch.append(u)
                
            tweet_obj['retweeted_status_id'] = rt.get('id')
            tweet_obj['is_retweet_status'] = True

        tweet_obj['source_type'] = source_type
        tweet_obj['source_id'] = source_id
        tweet_obj['user_id'] = tweet_obj['user']['id']
        tweet_batch.append(tweet_obj)
        user_batch.append(tweet_obj['user'])

    tweets = tweet_sc.load(tweet_batch, many=True)
    users = user_sc.load(user_batch, many=True)

    user_objs = [models.User(**user) for user in users]
    tweet_objs = [models.Tweet(**tweet) for tweet in tweets]

    try:
        logger.info(f"Adding {len(user_objs)} users to session")
        for i, u in enumerate(user_objs):
            if i % 5000 == 0:
                logger.info(f"User {i} of {len(user_objs)}")
            session.merge(u)

        logger.info(f"Adding {len(tweet_objs)} tweets to session")
        for i, t in enumerate(tweet_objs):
            if i % 5000 == 0:
                logger.info(f"Tweet {i} of {len(tweet_objs)}")
            session.merge(t)

        logger.info("Committing...")
        session.commit()
        logger.info("Done.")
    except Exception as e:
        logger.error(f"Error: {e}")
        session.rollback()
        raise
    finally:
        session.close()

def add_files(root_path):
    session = Session()
    path = Path(root_path)
    types = (
        'current-news',
        'trending-topics',
        'location-chile',
        'bounding-box',
        #'custom-keywords'
    )

    # iterate over types
    for name in types:
        files = []
        # iterate over dates
        for g in path.glob(f'{name}/*'):
            if not g.is_dir():
                continue
            # iterate over files
            for f in g.iterdir():
                files.append(f)

        source_id = None

        logger.info(f"({name}) Reading {len(files)} files...")
        for i, f in enumerate(sorted(files)):
            logger.info(f"({name}) File {i + 1} of {len(files)}")

            existing_file = session.query(models.LoadedFile).filter_by(path=f).first()
            if existing_file:
                logger.info(f"({name}) File {f} already exists. Skipping..")
                continue

            logger.info(f"({name}) Checking file {f}")
            if f.name.endswith('.txt'):
                with f.open() as g:
                    lines = [l[:-1] for l in g.readlines()]
                    keywords = ','.join(lines)

                    source = models.Source(name=name, keywords=keywords)
                    session.add(source)
                    lfile = models.LoadedFile(path=f, loaded=True)
                    session.add(lfile)

                    session.commit()
                    source_id = source.id
                    logger.info(f"({name}) Keyword file. Created source {source}")
                    logger.info(f"({name}) Created file {lfile}")

            elif f.name.endswith('.txt.gz'):
                # json file

                # f.name == 20191227_142911_news_stream.txt.gz
                # tokens[-1] == 'stream.txt.gz'
                # .split('.')[0] => 'stream'
                if name in ('trending-topics', 'current-news'):
                    tokens = f.name.split('_')
                    source_type = tokens[-1].split('.')[0]
                elif name in ('location-chile', 'bounding-box'):
                    source_type = 'stream'
                    source = session.query(models.Source).filter_by(name=name).first()
                    if source:
                        source_id = source.id
                    else:
                        source = models.Source(name=name)
                        session.add(source)
                        session.commit()
                        source_id = source.id
                with gzip.open(f, 'rb') as g:
                    save_file(path=f, file_=g, source_id=source_id, source_type=source_type)
                    lfile = models.LoadedFile(path=f, loaded=True)
                    session.add(lfile)
                    session.commit()
                    logger.info(f"({name}) Data file. Created file {lfile}")


if __name__ == '__main__':
    # path = Path('trending-topics/2019-12-18/20191218_185517_tt_search.txt')
    # save_file(path)
    
    # path = Path('current-news/2019-12-18/20191218_190800_news_stream.txt')
    # save_file(path)
    
    # path = Path('current-news/2019-12-18/2019-12-18_15-47-59_news_search.txt')
    # save_file(path)

    import sys
    p = sys.argv[1]

    add_files(Path(p))