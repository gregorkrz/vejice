from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from gensim.models import KeyedVectors
from sklearn.ensemble import GradientBoostingRegressor

import numpy as np


f1 = "models/sent_emb_lstm_POS_word2vec_20.emb"
f2 = "models/sent_emb_pos_lstm.emb"

pairs = [[], []]

wv1 = KeyedVectors.load_word2vec_format(f1, binary=False)
wv2 = KeyedVectors.load_word2vec_format(f2, binary=False)

vocab = list(wv1.vocab)
for sent_id in vocab:
    pairs[0].append(wv1[sent_id])
    pairs[1].append(wv2[sent_id])

pairs = np.array(pairs)

x, y = pairs[0, :, :], pairs[1, :, :]


#model_xy = GradientBoostingRegressor()
#model_yx = GradientBoostingRegressor()

model_xy = RandomForestRegressor(random_state=42)
model_yx = RandomForestRegressor(random_state=42)

model_xy.fit(x, y)
model_yx.fit(y, x)

pred_y = model_xy.predict(x)
pred_x = model_yx.predict(y)

score_xy = r2_score(y, pred_y)
score_yx = r2_score(x, pred_x)

print("score w2v-20dim POS -> 1-of-k POS", score_xy)
print("score 1-of-k POS -> w2v-20dim POS", score_yx)