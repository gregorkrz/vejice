from gensim.models import KeyedVectors
import random
import numpy as np

from server.library.db.stats import UserNotExistsException, getUserProfile


emb_file = "models/sent_emb_pos_lstm.emb" # sentence embeddings
emb = KeyedVectors.load_word2vec_format(emb_file, binary=False)
vocab = list(emb.vocab.keys())

LAST_K_RECOMMENDATION = 10

def softmax(numbers):
    e = np.exp(numbers)
    numbers = e / np.sum(e)
    return numbers


def recommend(user_id: str):
    try:
        profile = getUserProfile(user_id)
    except UserNotExistsException:
        profile = {}
    p, n = profile.get("positive_queue", []), profile.get("negative_queue", [])
    history = p + n
    p = p[-LAST_K_RECOMMENDATION:]
    n = n[-LAST_K_RECOMMENDATION:]
    if len(p) < 3 or len(n) < 3:
        return random.choice(vocab)
    neighbours = emb.most_similar(positive=n, negative=p, topn=len(history) + 10)
    probs = softmax([n[1] for n in neighbours if n[0] not in history])
    sents = [n[0] for n in neighbours if n[0] not in history]
    return np.random.choice(sents, p=probs)
