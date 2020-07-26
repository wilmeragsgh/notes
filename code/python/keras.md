---
description: Frecuently used code for keras
---

# Keras

**Save model**
```python
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")
```

**Load model**
```python
# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")
```

**Merging model**

```python
from keras.layers.merge import concatenate
from keras.models import Model, Sequential
from keras.layers import Dense, Input

model1_in = Input(shape=(27, 27, 1))
model1_out = Dense(300, input_dim=40, activation='relu', name='layer_1')(model1_in)
model1 = Model(model1_in, model1_out)

model2_in = Input(shape=(27, 27, 1))
model2_out = Dense(300, input_dim=40, activation='relu', name='layer_2')(model2_in)
model2 = Model(model2_in, model2_out)


concatenated = concatenate([model1_out, model2_out])
out = Dense(1, activation='softmax', name='output_layer')(concatenated)

merged_model = Model([model1_in, model2_in], out)
merged_model.compile(loss='binary_crossentropy', optimizer='adam', 
metrics=['accuracy'])

checkpoint = ModelCheckpoint('weights.h5', monitor='val_acc',
save_best_only=True, verbose=2)
early_stopping = EarlyStopping(monitor="val_loss", patience=5)

merged_model.fit([x1, x2], y=y, batch_size=384, epochs=200,
             verbose=1, validation_split=0.1, shuffle=True, 
callbacks=[early_stopping, checkpoint])
```

## References

- [Keras Transfer Learning For Beginners – Towards Data Science](https://towardsdatascience.com/keras-transfer-learning-for-beginners-6c9b8b7143e)