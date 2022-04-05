import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import Dropout

dataset = pd.read_csv("first_edit.csv")

x = dataset.drop(columns=['Decision','Already Bet'])
target = dataset['Decision']

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, target, test_size=0.2)

y_train = tf.keras.utils.to_categorical(y_train, 5)
y_test = tf.keras.utils.to_categorical(y_test, 5)


model = tf.keras.models.Sequential()


model.add(tf.keras.layers.Dense(128, activation='sigmoid'))
model.add(tf.keras.layers.Dense(64, activation='sigmoid'))
model.add(tf.keras.layers.Dense(5, activation='softmax'))


model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])



model.fit(x_train, y_train, epochs=1000)



model.evaluate(x_test,y_test)

model.save('11942014_2.h5')
