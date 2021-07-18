from sklearn.preprocessing import OneHotEncoder
import numpy as np


enc = OneHotEncoder()

pos_data = open("data/preprocessed/vejica_POS_raw.txt", "r")
pos = set()

line = True
while line:
    line = pos_data.readline()
    words = line.strip().split()
    pos.update(words)

pos = np.array(list(pos)).reshape(-1, 1)
enc.fit(pos)
emb = enc.transform(pos).toarray()

f = open("models/pos_embeddings.emb", "w")
f.write("{} {}\n".format(len(pos), len(pos)))

for i, p in enumerate(pos):
    f.write("{} {}\n".format(p[0], " ".join(emb[i].astype(str))))
f.close()