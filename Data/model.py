from keras.models import Model
from keras.layers import Input
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import GRU
import numpy as py
import keras
from loaddata import *

X1_train_stopfeatures,X2_train_headway,y_train_target_headway = get_train_dataset()

n_headway_features = 28
n_stop_features = X1_train_stopfeatures.shape[2]



n_units = 64

epochs = 30


learning_rate = 0.01
decay = 0 # Learning rate decay
optimiser = keras.optimizers.Adam(lr=learning_rate, decay=decay)

batch_size = 64

'''
# define training encoder
encoder_inputs = Input(shape=(None, n_stop_features))
encoder = LSTM(n_units, return_state=True)
encoder_outputs, state_h, state_c = encoder(encoder_inputs)
encoder_states = [state_h, state_c]
# define training decoder
decoder_inputs = Input(shape=(None, n_headway_features))
print(decoder_inputs)
print(decoder_inputs[:,:,0])

decoder_lstm = LSTM(n_units, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)


decoder_dense = Dense(n_headway_features,activation='relu')
decoder_outputs = decoder_dense(decoder_outputs)



model = Model(inputs = [encoder_inputs, decoder_inputs],outputs = decoder_outputs)
'''

encoder_inputs = Input(shape=(None, n_stop_features))
encoder = GRU(n_units, return_state=True)
encoder_outputs, state_h = encoder(encoder_inputs)

decoder_inputs = Input(shape=(None, n_headway_features))
decoder_gru = GRU(n_units, return_sequences=True)
decoder_outputs = decoder_gru(decoder_inputs, initial_state=state_h)
decoder_dense = Dense(n_headway_features,activation='relu')
decoder_outputs = decoder_dense(decoder_outputs)
model = Model([encoder_inputs, decoder_inputs], decoder_outputs)


model.compile(optimizer=optimiser, loss='mse',metrics=['acc'])

X1_test_stopfeatures,X2_test_headway,y_test_target_headway = get_test_dataset()

model.fit([X1_train_stopfeatures,X2_train_headway],y_train_target_headway,batch_size = batch_size,epochs = epochs,validation_split=0.2)


print('-------------------------------------------------------------')


x = model.predict([X1_test_stopfeatures,X2_test_headway])


allnum_real = 0
allnum_pre = 0
accnum = 0

offset = 0
allnum = 0

threshold_time = float(3/30)

for i in range(0,x.shape[0]):

    for index in range(0,n_headway_features):
        allnum+=1
        offset+=abs(list(y_test_target_headway[i,0,:])[index] - list(x[i,0,:])[index])
        if list(y_test_target_headway[i,0,:])[index] <= threshold_time:
            allnum_real+=1
        if list(x[i,0,:])[index] <= threshold_time:
            allnum_pre+=1
        if (list(x[i,0,:])[index] <= threshold_time) and (list(y_test_target_headway[i,0,:])[index] <= threshold_time):
            accnum+=1

print("allnum_real:")
print(allnum_real)
print("allnum_pre:")
print(allnum_pre)
print("accnum:")
print(accnum)


print()
print()
print(offset/allnum)



