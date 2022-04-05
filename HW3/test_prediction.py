import numpy as np
import tensorflow as tf

model = tf.keras.models.load_model('11942014.h5')
list_pred = [13,250,100,0,3]


i = model.predict([list_pred])

maxI = max(i[0])

index = np.where(i[0] == maxI)

print(index[0][0])