# Sample use case for finetuning

## Tags
#nlp 


```python
from transformers import BertTokenizer, TFBertModel

tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-uncased')

encoder = TFBertModel.from_pretrained("bert-base-multilingual-uncased")

##

class TextClassificationModel(tf.keras.Model):

	def __init__(self, encoder, n_classes):
		super(TextClassificationModel, self).__init__()
		self.encoder = encoder
		self.encoder.trainable = True
		self.dropout1 = tf.keras.layers.Dropout(0.1)
		self.dropout2 = tf.keras.layers.Dropout(0.1)
		self.dense1 = tf.keras.layers.Dense(20, activation="relu")
		self.dense2 = tf.keras.layers.Dense(n_classes, activation='softmax')

	def call(self, input):
		x = self.encoder(input)
		x = x['last_hidden_state'][:, 0, :]
		x = self.dropout1(x)
		x = self.dense1(x)
		x = self.dropout2(x)
		x = self.dense2(x)
		return x

##

train_encodings = tokenizer(X_train.tolist(), truncation=True, padding='max_length', max_length=512, return_tensors='tf')

##

import tensorflow as tf

train_dataset = tf.data.Dataset.from_tensor_slices((
	dict(train_encodings),
	y_train
))

##

text_classification_model = TextClassificationModel(encoder, len(labels_map.keys()))

##

text_classification_model.compile(
	tf.keras.optimizers.Adam(learning_rate=5e-5),
	loss="sparse_categorical_crossentropy",
	metrics=["accuracy"])
history = text_classification_model.fit(
	train_dataset.shuffle(1000).batch(16),
	epochs=3,
	# validation_data=val_dataset.batch(16),
	# callbacks=[tensorboard_callback]
)

```