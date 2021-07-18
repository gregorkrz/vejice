from sentence_autoencoder import *

#word_emb_file = "models/vejica_word2vec.emb"
#sentence_file = "data/preprocessed/lemmatized_with_name.txt"
#result_emb_file = "models/sentence_embeddings_lstm_test1707_5epochs.emb"

word_emb_file = "models/pos_embeddings.emb"
sentence_file = "data/preprocessed/vejica_POS_with_keys.txt"
result_emb_file = "models/sent_emb_pos_lstm.emb"


# construct timeseries from sentences
word_vectors = KeyedVectors.load_word2vec_format(word_emb_file, binary=False)
embsize = word_vectors.vector_size

sent = open(sentence_file, 'r').read().split('\n')

sent_emb = {}
for s in sent:
    a = s.split('\t')
    if len(a) != 2: continue
    a[1] = a[1].split(' ')
    sent_emb[a[0]] = np.array([word_vectors[word] for word in a[1] if word in word_vectors])

size = max([x.shape[0] for x in sent_emb.values()])

for s in sent_emb:
    #sent_emb[s].resize((size, embsize))
    sent_emb[s] = np.resize(sent_emb[s], (size, embsize))

train_data = np.array(list(sent_emb.values()))

np.random.seed(42)

from sklearn.model_selection import train_test_split

ae = SeqAutoEncoder(num_features=embsize, latent_space_dim=20, num_timesteps=size)
ae.fit_model('test0_POS_1epoch', train_data, epochs=1, batch_size=16)
#ae.load_model('test2_lstm__blocks__bs_256_ep_1saved-model-epoch_01.hdf5')

encoder = keras.Model(inputs=[ae.model.input], outputs=[ae.model.get_layer('lstm').output])
predictions = encoder(train_data)
sentence_names = list(sent_emb.keys())


print('writing sentence embeddings to file')
emb_out = open(result_emb_file, 'w')
emb_out.write('{} {}\n'.format(predictions.shape[0], predictions.shape[1]))
for i in range(len(sentence_names)):
    emb_out.write(sentence_names[i])
    emb_out.write(' ')
    emb_out.write(" ".join([str(k) for k in list(np.array(predictions[i]))]))
    emb_out.write('\n')
emb_out.close()