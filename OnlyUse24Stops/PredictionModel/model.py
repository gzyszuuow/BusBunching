from keras.models import Model
from keras.layers import Input
from keras.layers import LSTM
from keras.layers import Dense
import numpy as py
import keras


n_features = 28
n_units = 64


learning_rate = 0.01
decay = 0 # Learning rate decay
optimiser = keras.optimizers.Adam(lr=learning_rate, decay=decay)

batch_size = 64

# define training encoder
encoder_inputs = Input(shape=(None, n_features))
encoder = LSTM(n_units, return_state=True)
encoder_outputs, state_h, state_c = encoder(encoder_inputs)
encoder_states = [state_h, state_c]
# define training decoder
decoder_inputs = Input(shape=(None, n_features))
decoder_lstm = LSTM(n_units, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)
decoder_dense = Dense(n_features,activation='linear')
decoder_outputs = decoder_dense(decoder_outputs)
model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

model.compile(optimizer=optimiser, loss='mse')

