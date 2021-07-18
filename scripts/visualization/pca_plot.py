import numpy as np
from gensim.models import KeyedVectors
import plotly.express as px
from sklearn.decomposition import PCA
import pickle

#emb_file = "'models/sentence_embeddings_lstm_test1707_5epochs.emb"
emb_file = "models/sent_emb_pos_lstm.emb"

wv_from_text = KeyedVectors.load_word2vec_format(emb_file, binary=False)
#wv_from_text = KeyedVectors.load_word2vec_format('models/sentence_embeddings_lstm_test0.emb', binary=False)
#def display_pca_scatterplot(model, words=None, sample=0):
words = None
sample = 0
model = wv_from_text
if words == None:
    if sample > 0:
        words = np.random.choice(list(model.key_to_index.keys()), sample)
    else:
        words = [ word for word in model.vocab ]
    
word_vectors = np.array([model[w] for w in words])

twodim = PCA().fit_transform(word_vectors)[:,:2]

fig = px.scatter(x=twodim[:,0], y=twodim[:,1], hover_data={ 'snap-id': words})

fig.write_html('pca.html')