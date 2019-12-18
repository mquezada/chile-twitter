from pathlib import Path
import settings
import unidecode
#from sklearn.feature_extraction.text import CountVectorizer
import string
import spacy
import nltk
import textacy
from nltk.corpus import stopwords
from textacy import preprocessing
import re

from spacy.matcher import Matcher
from spacymoji import Emoji


nlp = spacy.load('es_core_news_sm')  # default
matcher = Matcher(nlp.vocab)
matcher.add('HASHTAG', None, [{'ORTH': '#'}, {'IS_ASCII': True}])
emoji = Emoji(nlp)
nlp.add_pipe(emoji, first=True)

sw = stopwords.words('spanish')
sw2 = spacy.lang.es.stop_words.STOP_WORDS

more_stopwords = [
    
]

sw = sw + more_stopwords

punct = string.punctuation + '“' + '”' + '¿' + '⋆' + '�'
URL_REGEX = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
DECIMAL_REGEX = '[0-9]+,[0-9]+'


# with Path(settings.GAZETTEER_PATH).open('r') as f:
#     comunas = set()
#     regiones = set()
#     for line in f:
#         tokens = [unidecode.unidecode(t) for t in line[:-1].split('\t')]
#         # to lower and remove accents
#         comunas.add(tuple(tokens[0].lower().split()))
#         regiones.add(tuple(tokens[1].lower().split()))

# regiones.add(tuple("bio-bio"))
# regiones.add(tuple("o'higgins"))
# comunas.remove(('los', 'angeles'))
# comunas.remove(('santa', 'cruz'))
# comunas.remove(('victoria', ))
# comunas.remove(('florida', ))


comunas = set()
for comuna in settings.COMUNAS_100:
    comuna = unidecode.unidecode(comuna)
    comuna = comuna.lower().split()
    comunas.add(tuple(comuna))


def is_sublist(large, small):
    if not large or not small:
        return False
    if len(small) > len(large):
        return False

    for i in range(len(large)):
        j = 0
        while large[i] == small[j]:
            i += 1
            j += 1
            # si termine con small, win!
            if j == len(small):
                return True
            # si no, y ya termine con large, loss
            if i == len(large):
                return False
    return False


def or_sublist(source, tests):
    for test in tests:
        if is_sublist(source, test):
            return True
    return False

exceptions = [
    ['argentina'],
    ['brasil'],
    ['espana'],
    ['paraguay'],
    ['uruguay'],
    ['santiago', 'del', 'estero'],
    ['santiago', 'de', 'compostela'],
    ['santiago', 'bernabeu'],
    ['colombia'],
    ['venezuela'],
    ['peru'],
    ['bolivia'],
    ['el', 'salvador'],
    ['cadiz'],  # colombia?
    ['mendoza'],
    ['mar', 'del', 'plata'],
    ['california'],
    ['ca'], # california
    ['valparaiso', 'de', 'goias'], # brasil
    ['tucuman'], # argentina
]

allowed = [
    ['chile'],
    ['🇨🇱'],
    ['scl']
]

def is_in_chile(location: str):
    try:
        loc = location.translate(str.maketrans('', '', string.punctuation))
        loc = unidecode.unidecode(loc.strip().lower()).split()
        if not loc:
            return False

        # if any of those appear...
        if or_sublist(loc, allowed):
            return True

        # then, if any of those appear...
        if or_sublist(loc, exceptions):
            return False

        # for region in regiones:
        #     if is_sublist(loc, region):
        #         return True

        for comuna in comunas:
            if is_sublist(loc, comuna):
                return True

        return False
    except Exception as e:
        print(e)
        return False


### tests
s = [
    'Los Angeles, Chile',
    'Recoleta',
    'Chile',
    ' Santiago. Chile ',
    'Chileno',
    'Soy de Chile',
    'santiaguino',
    'de talca con amor',
    'chiloe, talca, concepcion',
    'eeuu',
    'Florida, CA',
    'La Florida',
    'N.E. Florida & FL Keys',
    'Central Florida',
    'Clearwater Fla Florida NY'
]
# for ss in s:
#     print(is_in_chile(ss), ss, sep="\t")
#     print()


# cv = CountVectorizer(strip_accents='ascii')
# data = list(comunas) + list(regiones)
# vocab = cv.fit_transform(data)
# v = cv.transform(s)
# res = vocab.dot(v.T)
# import numpy as np
# idx = np.argmax(res, axis=0)
# for i in idx.tolist()[0]:
#     print(data[i])



def tokenize(doc,
             include_stopwords=False,
             include_punctuation=False,
             include_quotes=False,
             include_numbers=False,
             include_urls=False,
             lemmatize=False):

    try:
        tokens = nlp(" ".join(doc.split()))
    except:
        return []

    matches = matcher(tokens)
    hashtags = []
    for match_id, start, end in matches:
        hashtags.append(tokens[start:end])

    for span in hashtags:
        span.merge()

    processed = []
    for token in tokens:
        word = None
        if token.is_digit or re.match(DECIMAL_REGEX, token.lower_):
            word = "NUMBER" if include_numbers else None
        elif re.match(URL_REGEX, token.lower_):
            word = "URL" if include_urls else None
        elif token.is_stop or token.lower_ in sw:
            word = "STOPWORD" if include_stopwords else None
        elif (token.is_punct or token.lower_ in punct) and not token.is_quote:
            word = "PUNCT" if include_punctuation else None
        elif token.is_quote:
            word = "QUOTE" if include_quotes else None
        elif token._.is_emoji:
            word = None
        else:
            if lemmatize:
                word = token.lemma_
            else:
                word = token.text
            word = word.lower()
            word = word.strip()
            #word = preprocessing.remove_accents(word)

            if word.startswith(('@', '#')):
                word = ''

            word = word if word != '' else None

        if word:
            processed.append(word)
    return processed