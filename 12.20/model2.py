from keras.models import Model
from keras.layers import Input
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import GRU,Embedding,concatenate,Reshape
import numpy as np
import keras
#from loaddata2 import *

path1 = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\Test\\y_target_headway.npy"
path2 = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\Test\\X2_headways.npy"
path3 = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\Test\\X1_stopfeatures.npy"

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



#--------------------------------------------------------------------------------
x = []
while(len(x)<y_target_headway.shape[0]):
    x_ = np.random.randint(0,y_target_headway.shape[0],1)
    for val in x_:
        if val not in x:
            x.append(val)

y_target_headway = y_target_headway.tolist()
X2_headways = X2_headways.tolist()
StopID_shuffle = []
RoutesNum_shuffle = []
TimFeatures_shuffle = []
StopFeatures_shuffle = []
y_target_headway_shuffle = []
X2_headways_shuffle = []
for val in x:
    X2_headways_shuffle.append(X2_headways[val])
    y_target_headway_shuffle.append(y_target_headway[val])
    RoutesNum_shuffle.append(RoutesNum[val])
    TimFeatures_shuffle.append(TimFeatures[val])
    StopFeatures_shuffle.append(StopFeatures[val])
    StopID_shuffle.append(StopID[val])

#--------------------------------------------------------------------------------
#StopID = np.array(StopID)
#RoutesNum = np.array(RoutesNum)
#TimFeatures = np.array(TimFeatures)
#StopFeatures = np.array(StopFeatures)

X2_headways = np.array(X2_headways_shuffle)
y_target_headway = np.array(y_target_headway_shuffle)
RoutesNum = np.array(RoutesNum_shuffle)
TimFeatures = np.array(TimFeatures_shuffle)
StopFeatures = np.array(StopFeatures_shuffle)
StopID = np.array(StopID_shuffle)


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




'''
#Test Model
encoder_model = Model([StopIDInput,RoutesNumInput,TimFeatureInput,StopVarietyTimeFeaturesInput], encoder_states)
# define inference decoder
decoder_state_input_h = Input(shape=(n_units,))
decoder_state_input_c = Input(shape=(n_units,))
decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
decoder_outputs, state_h, state_c = decoder_lstm(decoder_inputs, initial_state=decoder_states_inputs)
decoder_states = [state_h, state_c]
decoder_outputs = decoder_dense(decoder_outputs)
decoder_model = Model([decoder_inputs] + decoder_states_inputs, [decoder_outputs] + decoder_states)
'''
#state = encoder_model.predict(source)

#------------------------------------------------------------------------------------------
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


