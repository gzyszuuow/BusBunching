from keras.models import Model
from keras.layers import Input
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import GRU,Embedding,concatenate
import numpy as np
import keras
#from loaddata2 import *

path1 = "/Users/gongcengyang/Desktop/y_target_headway.npy"
path2 = "/Users/gongcengyang/Desktop/X2_headways.npy"
path3 = "/Users/gongcengyang/Desktop/X1_stopfeatures.npy"

y_target_headway = np.load(path1)
X2_headways = np.load(path2)
X1_stopfeatures = np.load(path3)

StopID = []
RoutesNum = []
TimFeatures = []
StopFeatures = []

for i in range(X1_stopfeatures.shape[0]):
    ls1 = []
    ls2 = []
    ls3 = []
    ls4 = []
    for index in range(0,28):
        ls1_each = []
        ls2_each = []
        ls3_each = []
        ls4_each = []

        l = list(X1_stopfeatures[i][index])

        ls1_each.append(l[0])
        ls2_each.append(l[1])
        ls3_each.append(l[3])

        for i in range(X1_stopfeatures.shape[2]):
            if i not in [0,1,3]:
                ls4_each.append(l[i])
        ls4.append(ls4_each)

        ls1.append(ls1_each)
        ls2.append(ls2_each)
        ls3.append(ls3_each)
    StopID.append(ls1)
    RoutesNum.append(ls2)
    TimFeatures.append(ls3)
    StopFeatures.append(ls4)


StopID = np.array(StopID)
RoutesNum = np.array(RoutesNum)
TimFeatures = np.array(TimFeatures)
StopFeatures = np.array(StopFeatures)

print(StopID.shape)
print(RoutesNum.shape)
print(TimFeatures.shape)
print(StopFeatures.shape)

n_headway_features = 28
n_stop_features = X1_stopfeatures.shape[2]

n_units = 64
epochs = 30

learning_rate = 0.01
decay = 0 # Learning rate decay
optimiser = keras.optimizers.Adam(lr=learning_rate, decay=decay)

batch_size = 5


# define training encoder
#encoder_inputs = Input(shape=(None, n_stop_features))
Input1 = Input(shape=(28,1))
Input2 = Input(shape=(28,1))
Input3 = Input(shape=(28,1))
Input4 = Input(shape=(28,8))
embed1 = Embedding(28,4)(Input1)
embed2 = Embedding(96,4)(Input2)
embed3 = Embedding(3,4)(Input3)
encoder_inputs = concatenate([embed1, embed2,embed3,Input4],axis=-1)

encoder = LSTM(n_units, return_state=True)
encoder_outputs, state_h, state_c = encoder(encoder_inputs)
encoder_states = [state_h, state_c]
# define training decoder
decoder_inputs = Input(shape=(None, n_headway_features))
decoder_lstm = LSTM(n_units, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)
decoder_dense = Dense(n_headway_features,activation='relu')
decoder_outputs = decoder_dense(decoder_outputs)

#model = Model(inputs = [encoder_inputs, decoder_inputs],outputs = decoder_outputs)
#model.fit([X1_train_stopfeatures,X2_train_headway],y_train_target_headway,batch_size = batch_size,epochs = epochs,validation_split=0.2)
model = Model(inputs = [Input1,Input2,Input3,Input4,decoder_inputs],outputs = decoder_outputs)
model.compile(optimizer=optimiser, loss='mse')
model.fit([StopID,RoutesNum,TimFeatures,StopFeatures,X2_headways],y_target_headway)



'''
n_headway_features = 28
n_stop_features = X1_stopfeatures.shape[2]



n_units = 64

epochs = 30


learning_rate = 0.01
decay = 0 # Learning rate decay
optimiser = keras.optimizers.Adam(lr=learning_rate, decay=decay)

batch_size = 64


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




#model.fit([X1_train_stopfeatures,X2_train_headway],y_train_target_headway,batch_size = batch_size,epochs = epochs,validation_split=0.2)


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

'''

from keras.layers import Input
from keras.layers import Embedding
from keras.layers import LSTM

import keras

inputs = [(42, 0.5, 0.6), (36, 0.4, 0.7), (50, 0.2, 0.9)] # example. The real data is a sequence of millions of tuples

intInputs = np.array([el[0] for el in inputs])    
floatInputs = np.array([el[1],el[2]] for el in inputs)

print(intInputs.shape)
print(floatInputs.shape)
print("------------------")
'''
input_id = Input(shape=(1,), dtype='int32', name='input_type') # id is within [0, 99]
embed_id = Embedding(output_dim=3, input_dim=20, input_length=1)(input_id)

input_v1 = Input(shape=(1,), dtype='float', name='input_v1')
input_v2 = Input(shape=(1,), dtype='float', name='input_v2')

input_merged = keras.layers.concatenate([embed_id, input_v1, input_v2], axis=-1)

lstm = LSTM(40) # how do I tell it to use input_merged as input ?
'''
