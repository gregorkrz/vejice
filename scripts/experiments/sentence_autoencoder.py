import keras
from keras.layers import Input, LSTM, Dense, RepeatVector, TimeDistributed
from keras.models import Sequential
from keras import backend as K
import numpy as np
from keras.callbacks import ModelCheckpoint
from gensim.models import KeyedVectors


class SeqAutoEncoder:
    def __enter__(self):
        return self
    def __init__(self, num_timesteps=10, num_features=10, latent_space_dim=30):
        self.initial_value = 0  # constant
        self.num_features = num_features
        self.latent_space_dim = 30
        self.num_timesteps = num_timesteps
        inp = Input(shape=(self.num_timesteps, self.num_features))
        lstm_enc = LSTM(self.latent_space_dim, activation='tanh')(inp)
        r = RepeatVector(self.num_timesteps)(lstm_enc)
        lstm_dec = LSTM(self.latent_space_dim, return_sequences=True, activation='tanh')(r)
        out = TimeDistributed(Dense(self.num_features))(lstm_dec)
        self.model = keras.Model(inp, out)
        self.model.compile(optimizer='adam', loss='mse')
        self.model.summary()

    def fit_model(self, exp_label, timeseries, epochs=2, batch_size=8, validation_split=0.2):
        exp_name = exp_label + '_lstm__blocks__bs_{}_ep_{}'.format( batch_size, epochs)
        filepath = exp_name + "saved-model-epoch_{epoch:02d}.hdf5"
        checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=False, mode='max')
        history = self.model.fit(timeseries, timeseries,
                                 batch_size=batch_size,
                                 epochs=epochs,
                                 validation_split=validation_split,
                                 verbose=1,
                                 callbacks=[checkpoint])
        #self.model.save(exp_name)
        fname = exp_name + '_HISTORY_obj.txt'
        #print(history.history)
        f = open(fname, "a")
        f.write(str(history.history))
        f.close()
        

    def load_model(self, filename):
        self.model = keras.models.load_model(filename)
        #self.model.summary()

    def predict(self, data):
        return self.model.predict(data, verbose=1)


