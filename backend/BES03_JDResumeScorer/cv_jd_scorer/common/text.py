import re
import string

import nltk
from nltk.corpus import stopwords

nltk.download("stopwords", quiet=True)
nltk.download("punkt_tab", quiet=True)

_STOP = set(stopwords.words("english"))


# -------------------- tokenize ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: remove_stopwords, extract_top_keywords
def tokenize(text: str) -> list[str]:
    text = text.lower()
    text = re.sub(r"[" + re.escape(string.punctuation) + r"]", " ", text)
    return [t for t in text.split() if t]
# -------------------- tokenize ------------- END ----------------


# -------------------- remove_stopwords ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: extract_top_keywords
def remove_stopwords(tokens: list[str]) -> list[str]:
    return [t for t in tokens if t not in _STOP and len(t) > 1]
# -------------------- remove_stopwords ------------- END ----------------


# -------------------- extract_top_keywords ----------- START ----------
# -- Calls : tokenize, remove_stopwords
# -- Called by: engines that need keyword extraction
def extract_top_keywords(text: str, n: int = 30) -> list[str]:
    tokens = remove_stopwords(tokenize(text))
    freq: dict[str, int] = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1
    return sorted(freq, key=lambda k: freq[k], reverse=True)[:n]
# -------------------- extract_top_keywords ------------- END ----------------
