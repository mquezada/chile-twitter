import datetime 
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()

def parse_twitter_date(created_at):
    #  'Thu Dec 12 17:27:03 +0000 2019'
    dt = datetime.datetime.strptime(created_at, '%a %b %d %H:%M:%S %z %Y')
    return dt


class Tweet(Base):
    __tablename__ = 'tweet'

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime)
    text = Column(String(280))
    source = Column(String(512))
    truncated = Column(Boolean)
    in_reply_to_status_id = Column(BigInteger)
    in_reply_to_user_id = Column(BigInteger)
    in_reply_to_screen_name = Column(String(50))
    coordinates = Column(String(280))
    place = Column(String(1024))
    quoted_status_id = Column(BigInteger)
    retweeted_status_id = Column(BigInteger)
    is_quote_status = Column(Boolean)
    is_retweet_status = Column(Boolean)
    quote_count = Column(Integer)
    retweet_count = Column(Integer)
    favorite_count = Column(Integer)
    reply_count = Column(Integer)
    entities = Column(String(4096))
    extended_entities = Column(String(4096))
    possibly_sensitive = Column(Boolean)
    filter_level = Column(String(32))
    lang = Column(String(32))
    
    user_id = Column(BigInteger, ForeignKey('user.id'))

    timestamp_added_utc = Column(DateTime, default=datetime.datetime.utcnow)
    source_type = Column(String(32))

    def __repr__(self):
        text = ' '.join(self.text.strip())
        return f"<Tweet(id={self.id}, text='{text}')>"

class SourceTweet(Base):
    __tablename__ = 'source_tweet'

    id = Column(Integer, primary_key=True)
    tweet_id = Column(BigInteger, ForeignKey('tweet.id'))
    source_id = Column(Integer, ForeignKey('source.id'))


class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(50))
    screen_name = Column(String(128))
    location = Column(String(256))
    url = Column(String(256))
    description = Column(String(280))
    protected = Column(Boolean)
    verified = Column(Boolean)
    followers_count = Column(Integer)
    friends_count = Column(Integer)
    listed_count = Column(Integer)
    favourites_count = Column(Integer)
    statuses_count = Column(Integer)
    created_at = Column(DateTime)
    default_profile = Column(Boolean)
    default_profile_image = Column(Boolean)

    tweets = relationship('Tweet')

    timestamp_added_utc = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<User(id={self.id}, name=@{self.screen_name})>"

class Source(Base):
    __tablename__ = "source"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    keywords = Column(String(2048))

    timestamp_added_utc = Column(DateTime, default=datetime.datetime.utcnow)
    tweets = relationship('Tweet')

    def __repr__(self):
        return f"<Source(name={self.name})>"

class LoadedFile(Base):
    __tablename__ = 'loaded_file'

    id = Column(Integer, primary_key=True)
    path = Column(String(128), unique=True)
    loaded = Column(Boolean, default=False)
    timestamp_added_utc = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<LoadedFile(loaded={self.loaded}, path={self.path})>"