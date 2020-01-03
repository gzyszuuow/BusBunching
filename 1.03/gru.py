from keras.models import Model
from keras.layers import Input
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import GRU,Embedding,concatenate,Reshape
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
import numpy as np
import keras
from loaddata_gru import *

X2_train_headway,y_train_target_headway = get_train_dataset()


print(X2_train_headway.shape)
print(y_train_target_headway.shape)

X2_train_headway = X2_train_headway.reshape(X2_train_headway.shape[0],-1)
y_train_target_headway = y_train_target_headway.reshape(-1,28)

print(X2_train_headway.shape)
print(y_train_target_headway.shape)

learning_rate = 0.01
decay = 0 # Learning rate decay
optimiser = keras.optimizers.Adam(lr=learning_rate, decay=decay)
input1 = Input(shape=(28,))
dens1 = Dense(128,activation="relu")(input1)
dro1 = Dropout(0.2)(dens1)
dens2 = Dense(64,activation="relu")(dro1)
dro2 = Dropout(0.2)(dens2)
pre = Dense(28,activation="relu")(dro2)

model = Model(inputs = input1,outputs = pre)
model.compile(optimizer=optimiser, loss='mse',metrics=['acc'])
model.fit(X2_train_headway,y_train_target_headway,batch_size = 64,epochs = 5,validation_split=0.1)

'''
n_headway_features = 28


n_units = 64
epochs = 10

learning_rate = 0.01
decay = 0 # Learning rate decay
optimiser = keras.optimizers.Adam(lr=learning_rate, decay=decay)

batch_size = 64

MaxStopID = 27
MaxRoutesNum = 95
MaxTimeFeature = 3
StopNumber = 28

#define training encoder
StopIDInput = Input(shape=(StopNumber,1))
RoutesNumInput = Input(shape=(StopNumber,1))
TimFeatureInput = Input(shape=(StopNumber,1))

StopIDInputEmbed = Embedding(MaxStopID+1,4)(StopIDInput)
RoutesNumInputembed = Embedding(MaxRoutesNum+1,4)(RoutesNumInput)
TimFeatureInputembed = Embedding(MaxTimeFeature+1,4)(TimFeatureInput)
StopVarietyTimeFeaturesInput = Input(shape=(StopNumber,n_stop_features - 3))

StopIDInputEmbed = Reshape((StopNumber,4))(StopIDInputEmbed)
RoutesNumInputembed = Reshape((StopNumber,4))(RoutesNumInputembed)
TimFeatureInputembed = Reshape((StopNumber,4))(TimFeatureInputembed)

encoder_inputs = concatenate([StopIDInputEmbed, RoutesNumInputembed,TimFeatureInputembed,StopVarietyTimeFeaturesInput],axis=-1)
encoder = LSTM(n_units, return_state=True)
encoder_outputs, state_h, state_c = encoder(encoder_inputs)
encoder_states = [state_h, state_c]
# define training decoder
decoder_inputs = Input(shape=(None, n_headway_features))
decoder_lstm = LSTM(n_units, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)
decoder_dense = Dense(n_headway_features,activation='relu')
decoder_outputs = decoder_dense(decoder_outputs)

model = Model(inputs = [StopIDInput,RoutesNumInput,TimFeatureInput,StopVarietyTimeFeaturesInput,decoder_inputs],outputs = decoder_outputs)
model.compile(optimizer=optimiser, loss='mse',metrics=['acc'])
model.fit([StopID,RoutesNum,TimFeatures,StopFeatures,X2_headways],y_target_headway,batch_size = batch_size,epochs = epochs,validation_split=0.1)



x = model.predict([StopID,RoutesNum,TimFeatures,StopFeatures,X2_headways])
allnum_real = 0
allnum_pre = 0
accnum = 0
offset = 0
allnum = 0
threshold_time = float(3/30)
for i in range(0,x.shape[0]):
    for index in range(0,n_headway_features):
        allnum+=1
        offset+=abs(list(y_target_headway[i,0,:])[index] - list(x[i,0,:])[index])
        if list(y_target_headway[i,0,:])[index] <= threshold_time:
            allnum_real+=1
        if list(x[i,0,:])[index] <= threshold_time:
            allnum_pre+=1
        if (list(x[i,0,:])[index] <= threshold_time) and (list(y_target_headway[i,0,:])[index] <= threshold_time):
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



