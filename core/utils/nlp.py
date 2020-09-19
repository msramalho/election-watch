import re, string
from nltk.corpus import stopwords


def remove_emojis(data):  # https://stackoverflow.com/a/58356570/6196010
    emojis = re.compile("["
                        u"\U0001F600-\U0001F64F"  # emoticons
                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                        u"\U00002500-\U00002BEF"  # chinese char
                        u"\U00002702-\U000027B0"
                        u"\U00002702-\U000027B0"
                        u"\U000024C2-\U0001F251"
                        u"\U0001f926-\U0001f937"
                        u"\U00010000-\U0010ffff"
                        u"\u2640-\u2642"
                        u"\u2600-\u2B55"
                        u"\u200d"
                        u"\u23cf"
                        u"\u23e9"
                        u"\u231a"
                        u"\ufe0f"  # dingbats
                        u"\u3030"  "]+", re.UNICODE)
    return re.sub(emojis, '', data)


NLP_STOPWORDS = set(stopwords.words("portuguese") + stopwords.words("english") + stopwords.words("spanish") + stopwords.words("italian") + stopwords.words("french"))


def nlp_preprocess(doc, _stopwords=None, keep_hashtags=True):
    doc = doc.lower()
    doc = re.sub(r'http\S+', '', doc)  # urls
    doc = re.sub(r'[0-9]+', '', doc)  # numbers
    doc = re.sub(r'@\w{1,15}', '', doc)  # mentions
    if keep_hashtags: doc = re.sub(r'#', '', doc)
    else: doc = re.sub(r'#\w+', '', doc)  # remove hashtags
    doc = re.sub(r'\n+', ' ', doc)  # newlines
    doc = doc.translate(str.maketrans('', '', string.punctuation + "“”"))
    doc = remove_emojis(doc)
    doc = re.sub(r'⃣', '', doc)
    doc = filter(len, doc.split(" "))
    if not _stopwords: _stopwords = NLP_STOPWORDS
    doc = filter(lambda word: word not in _stopwords, doc)
    return " ".join(doc)


# def get_tokens(doc, stopwords=set()):
#     tokens = filter(len, doc.split(""))
#     no_stopwords = filter(lambda word: word not in stopwords, tokens)
#     return list(no_stopwords)
