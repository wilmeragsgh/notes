---
description: Frequently used code for tensorflow related code snippets
---

# Tensorflow

**General steps**

* Create Tensors \(variables\) that are not yet executed/evaluated.
* Write operations between those Tensors.
* Initialize your Tensors.
* Create a Session.
* Run the Session. This will run the operations you'd written above.

> Tensorflow has a lot of functions already implemented

## One-liners

* `tf.sigmoid`
* `tf.nn.sigmoid_cross_entropy_with_logits` 
* `tf.ones`
* `tf.zeros_initializer`
* `tf.contrib.layers.xavier_initializer(seed = 1)`
* `tf.nn.relu`
* `tf.add`
* `tf.matmul`
* `tf.transpose`

## Recipes

**Installing**

`import tensorflow as tf`

**Set different types of values**

```python
c = tf.constant(12,name="c")
x = tf.get_variable(c**2,name='x') # variable, could have shape=[x,y], and initializer=
y = tf.placeholder(tf.int64, name = 'x') # placeholder is a value you can specify at the moment of the session execution with the parameter feed_dict = {x: 3}
# Placeholder could have shape as shape=[n_x,None]
```

**Initialize variables**

```python
tf.reset_default_graph()
# Above code seems to be a good practice
init = tf.global_variable_initializer()
with tf.Session() as sess:
    sess.run(init)

# if not used with 'with' it is necessary to do sess.close()
```

**Computing cost for sigmoid**

```python
cost = tf.nn.sigmoid_cross_entropy_with_logits(logits=z,labels=y)# z = \hat{y} and y = true value of label
```

**One-hot encoding**

```python
one_hot_matrix = tf.one_hot(labels,C, axis=0)# C is number classes, labels is vector of labels
```

**Given a cost function**

```python
tf.train.AdamOptimizer(learning_rate = learning_rate).minimize(cost)
```

```python
# Calculate the correct predictions
correct_prediction = tf.equal(tf.argmax(Z3), tf.argmax(Y))
# Calculate accuracy on the test set
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
print("Train Accuracy:", accuracy.eval({X: X_train, Y: Y_train}))
print("Test Accuracy:", accuracy.eval({X: X_test, Y: Y_test}))
```

## Convolutions

##### Input

- M: 2d-Tensor with real values (where we will apply the convolution)
- K: Smaller 2d-tensor with real values (the convolution kernel)


##### Process

1. Multiply each entry of the 2d-tensor K with each one on the 2d-tensor M 


I think they could be affected by the resolution of the images

**conv2d**

```python
tf.nn.conv2d(X,W, strides = [1,s,s,1], padding = 'SAME')
```

> **Use:** Computing convolutions of W kernel over X with a stride over 1st and 4th dimension\(batch dimension ie: one example, and 1 channel\)

**max\_pool**

```python
tf.nn.max_pool(A, ksize = [1,f,f,1], strides = [1,s,s,1], padding = 'SAME')
```

> **Use:** Given an input A it performs a pooling layer with a windown of size \(f,f\), ie usually it takes one example and one channel at a time.

**flatten**

```python
tf.contrib.layers.flatten(P)
```

> **Use:** Given an input tensor P it takes each example from batch and generate an 1D array as output For example, receiving a tensor of shape \[batch\_size, width, height, channels\] it would return a tensor of shape = \[batch\_size, width x height x channels\]

**fully\_connected**

```python
tf.contrib.layers.fully_connected(F, num_outputs)
```

> **Use:** Given an input tensor F \(flattened\) it generates an initialized layer of weights in the graph, so they don't need to be initialized. This layers needs to have an additional argument `activation_fn=None` to not apply softmax

**Cost computation**

```python
tf.nn.softmax_cross_entropy_with_logits(logits = Z, labels = Y)
```

```python
tf.reduce_mean
```

> "Logits" are the result of multiplying the weights and adding the biases. Logits are passed through an activation function \(such as a relu\), and the result is called the "activation."
>
> Example of functional code for a tf project is at docs/career/convnet\_course




#### Images
##### Read functions

```python
from tensorflow.python.keras.preprocessing.image import load_img,img_to_array

imgs = [load_img(img_path, target_size=(img_height, img_width)) for img_path in img_paths]
    img_array = np.array([img_to_array(img) for img in imgs])

```

##### ResNet50 preprocessing
```python
from tensorflow.python.keras.applications.resnet50 import preprocess_input
output = preprocess_input(img_array)
```

##### Utils
```python
from keras.applications.resnet50 import decode_predictions
decode_predictions(preds, top=3) # model.predict output
```

##### Display on notebook
```python
from IPython.display import Image,display
display(Image(img_path))
```

##### Transfer learning example
```python
from tensorflow.python.keras.applications import ResNet50
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Flatten, GlobalAveragePooling2D

num_classes = 2
resnet_weights_path = '../input/resnet50/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5'

my_new_model = Sequential()
my_new_model.add(ResNet50(include_top=False, pooling='avg', weights=resnet_weights_path))
my_new_model.add(Dense(num_classes, activation='softmax'))

# Say not to train first layer (ResNet) model. It is already trained
my_new_model.layers[0].trainable = False
```

##### Feeding data into models with ImageGenerator
```python
from tensorflow.python.keras.applications.resnet50 import preprocess_input
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator

image_size = 224
data_generator = ImageDataGenerator(preprocessing_function=preprocess_input)

# having 72 images for training and 20 for validation
train_generator = data_generator.flow_from_directory(
        '../input/urban-and-rural-photos/rural_and_urban_photos/train',
        target_size=(image_size, image_size),
        batch_size=24,
        class_mode='categorical')

validation_generator = data_generator.flow_from_directory(
        '../input/urban-and-rural-photos/rural_and_urban_photos/val',
        target_size=(image_size, image_size),
        class_mode='categorical')

my_new_model.fit_generator(
        train_generator,
        steps_per_epoch=3,
        validation_data=validation_generator,
        validation_steps=1)
```