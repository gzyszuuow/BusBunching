from keras.models import Model
from keras.layers import Input
from keras.layers import LSTM
from keras.layers import Dense
import numpy as py
import keras
from test_loaddata import *

#X1_train_stopfeatures,X2_train_headway,y_train_target_headway = get_train_dataset()

X2_train_headway,X1_train_stopfeatures,y_train_target_headway = get_dataset()

X2_train_headway=np.array(X2_train_headway)
X1_train_stopfeatures=np.array(X1_train_stopfeatures)
y_train_target_headway=np.array(y_train_target_headway)

print(X2_train_headway.shape)
print(X1_train_stopfeatures.shape)
print(y_train_target_headway.shape)



n_headway_features = 28
n_stop_features = X1_train_stopfeatures.shape[2]



n_units = 64

epochs = 30


learning_rate = 0.01
decay = 0 # Learning rate decay
optimiser = keras.optimizers.Adam(lr=learning_rate, decay=decay)

batch_size = 128

# define training encoder
encoder_inputs = Input(shape=(None, n_stop_features))
encoder = LSTM(n_units, return_state=True)
encoder_outputs, state_h, state_c = encoder(encoder_inputs)
encoder_states = [state_h, state_c]
# define training decoder
decoder_inputs = Input(shape=(None, n_headway_features))
decoder_lstm = LSTM(n_units, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)


decoder_dense = Dense(n_headway_features,activation='relu')
decoder_outputs = decoder_dense(decoder_outputs)

#,activation='tanh'

model = Model(inputs = [encoder_inputs, decoder_inputs],outputs = decoder_outputs)

model.compile(optimizer=optimiser, loss='mse',metrics=['acc'])


model.fit([X1_train_stopfeatures,X2_train_headway],y_train_target_headway,batch_size = batch_size,epochs = epochs)


print('-------------------------------------------------------------')
'''
X1_test_stopfeatures,X2_test_headway,y_test_target_headway = get_test_dataset()


x = model.predict([X1_test_stopfeatures,X2_test_headway])


allnum_real = 0
allnum_pre = 0
accnum = 0

offset = 0
allnum = 0

threshold_time = float(5/30)

for i in range(0,x.shape[0]):
    #print(i)
    #print("Pre:")
    #print(list(x[i,0,:]))
    #print("Real:")
    #print(list(y_test_target_headway[i,0,:]))
    #print()

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
'''


'''
print(X1_test_stopfeatures.shape)
print(X2_test_headway.shape)
print(y_test_target_headway.shape)

for i in range(0,y_test_target_headway.shape[0]):
    print(X1_test_stopfeatures[i].shape)
    print(X2_test_headway[i].shape)
    print(y_test_target_headway[i].shape)

    X1_test_stopfeatures[i].reshape(1,X1_test_stopfeatures[i].shape[0],X1_test_stopfeatures[i].shape[1])
    X2_test_headway[i].reshape(1,X2_test_headway[i].shape[0],X2_test_headway[i].shape[1])


    print(model.predict([X1_test_stopfeatures[i],X2_test_headway[i]]))
    break
'''