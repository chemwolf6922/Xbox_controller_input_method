import numpy as np
import string
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pylab as pl

labels = []
data = []

with open('log/data','r') as f:
    for line in f:
        if line.strip('\n') in string.ascii_uppercase:
            labels.append(line.strip('\n'))
            data.append([])
        else:
            data[-1].append([int(i) for i in line.strip('\n').split(',')])

train_labels = []
train_data = []

alphabet = np.array(list(string.ascii_uppercase))

for l in labels:
    train_labels.append(l == alphabet)

train_labels = np.asarray(train_labels,dtype = np.float32)

for d in data:
    temp = d[0]
    if (temp[0]**2+temp[1]**2)**0.5 < (temp[2]**2+temp[3]**2)**0.5:
        temp[0] = 0
        temp[1] = 0
    else:
        temp[2] = 0
        temp[3] = 0
    train_data.append(temp)

train_data = np.asarray(train_data,dtype = np.float32)

# print(train_data[:5])
# print(train_labels[:5])
# print(labels[:5])

inputs = keras.Input(shape = (4))
outputs = layers.Dense(26,activation = 'softmax')(inputs)

silly = keras.Model(inputs = inputs,outputs = outputs)
silly.compile(optimizer = 'adam',loss = keras.losses.CategoricalCrossentropy(),metrics = ['acc'])

silly.summary()

history = silly.fit(train_data,train_labels,batch_size=640,epochs = 1000,verbose = 0,shuffle = True)

silly.save('classifier.h5')

pl.plot(history.history['acc'])
pl.show()


