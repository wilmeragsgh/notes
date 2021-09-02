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

#### Input

* M: 2d-Tensor with real values \(where we will apply the convolution\)
* K: Smaller 2d-tensor with real values \(the convolution kernel\)

#### Process

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

### Images

#### Read functions

```python
from tensorflow.python.keras.preprocessing.image import load_img,img_to_array

imgs = [load_img(img_path, target_size=(img_height, img_width)) for img_path in img_paths]
    img_array = np.array([img_to_array(img) for img in imgs])
```

#### ResNet50 preprocessing

```python
from tensorflow.python.keras.applications.resnet50 import preprocess_input
output = preprocess_input(img_array)
```

#### Utils

```python
from keras.applications.resnet50 import decode_predictions
decode_predictions(preds, top=3) # model.predict output
```

#### Display on notebook

```python
from IPython.display import Image,display
display(Image(img_path))
```

#### Transfer learning example

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

#### Feeding data into models with ImageGenerator

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

#### TPU usage

```python
%tensorflow_version 2.x
import tensorflow as tf
try:
  tpu = tf.distribute.cluster_resolver.TPUClusterResolver()  # TPU detection
  print('Running on TPU ', tpu.cluster_spec().as_dict()['worker'])
except ValueError:
  raise BaseException('ERROR: Not connected to a TPU runtime; please see the previous cell in this notebook for instructions!')
tf.config.experimental_connect_to_cluster(tpu)
tf.tpu.experimental.initialize_tpu_system(tpu)
tpu_strategy = tf.distribute.experimental.TPUStrategy(tpu)
```

When training:

```python
with tpu_strategy.scope():
    full_model = create_model(max_words, embedding_dim, max_len, embedding_matrix)
    history = full_model.fit(X_train, Y_train, epochs = 14)
```

## TFX

### TFDV

**References**

- https://www.tensorflow.org/tfx/data_validation/get_started
- https://blog.tensorflow.org/2018/09/introducing-tensorflow-data-validation.html
- https://colab.research.google.com/github/tensorflow/tfx/blob/master/docs/tutorials/data_validation/tfdv_basic.ipynb#scrollTo=mPt5BHTwy_0F
- https://www.tensorflow.org/tfx/data_validation/api_docs/python/tfdv

**Import**

```python
import tensorflow as tf
import tensorflow_data_validation as tfdv
import pandas as pd
from tensorflow_metadata.proto.v0 import schema_pb2


print('TFDV Version: {}'.format(tfdv.__version__))
print('Tensorflow Version: {}'.format(tf.__version__))
```

**Generate statistics**

```python
# Generate training dataset statistics
train_stats = tfdv.generate_statistics_from_dataframe(train_df)
```

**Visualize statistics**

```python
# Visualize training dataset statistics
tfdv.visualize_statistics(train_stats)
```

**Infer data schema**

```python
# Infer schema from the computed statistics.
schema = tfdv.infer_schema(statistics=train_stats)

# Display the inferred schema
tfdv.display_schema(schema)
```

**Comparing stats from training/test**

```python
# Generate evaluation dataset statistics
eval_stats = tfdv.generate_statistics_from_dataframe(eval_df)

# Compare training with evaluation
tfdv.visualize_statistics(
    lhs_statistics=eval_stats, 
    rhs_statistics=train_stats, 
    lhs_name='EVAL_DATASET', 
    rhs_name='TRAIN_DATASET'
)
```

**Calculate and display anomalies**

```python
# Check evaluation data for errors by validating the evaluation dataset statistics using the reference schema
anomalies = tfdv.validate_statistics(statistics=eval_stats, schema=schema)

# Visualize anomalies
tfdv.display_anomalies(anomalies)
```

**Fix anomalies in the schema**

```python
# Relax the minimum fraction of values that must come from the domain for the feature `native-country`
country_feature = tfdv.get_feature(schema, 'native-country')
country_feature.distribution_constraints.min_domain_mass = 0.9

# Relax the minimum fraction of values that must come from the domain for the feature `occupation`
occupation_feature = tfdv.get_feature(schema, 'occupation')
occupation_feature.distribution_constraints.min_domain_mass = 0.9
```

**More flexible extension of schema**

```python
# Add new value to the domain of the feature `race`
race_domain = tfdv.get_domain(schema, 'race')
race_domain.value.append('Asian')
```

**Manual set of range for int values**

```python
# Restrict the range of the `age` feature
tfdv.set_domain(schema, 'age', schema_pb2.IntDomain(name='age', min=17, max=90))

# Display the modified schema. Notice the `Domain` column of `age`.
tfdv.display_schema(schema)
```

**Data slicing**

```python
from tensorflow_data_validation.utils import slicing_util

# features={'sex': [b'Male']} # or this for example (with b'')
slice_fn = slicing_util.get_feature_value_slicer(features={'sex': None})

# Declare stats options
slice_stats_options = tfdv.StatsOptions(schema=schema,
                                        slice_functions=[slice_fn],
                                        infer_type_from_schema=True)


# Convert dataframe to CSV since `slice_functions` works only with `tfdv.generate_statistics_from_csv`
CSV_PATH = 'slice_sample.csv'
train_df.to_csv(CSV_PATH)

# Calculate statistics for the sliced dataset
sliced_stats = tfdv.generate_statistics_from_csv(CSV_PATH, stats_options=slice_stats_options)

from tensorflow_metadata.proto.v0.statistics_pb2 import DatasetFeatureStatisticsList


#  An important caveat is visualize_statistics() accepts a DatasetFeatureStatisticsList type instead of DatasetFeatureStatistics. Thus, at least for this version of TFDV, you will need to convert it to the correct type.

# Convert `Male` statistics (index=1) to the correct type and get the dataset name
male_stats_list = DatasetFeatureStatisticsList()
male_stats_list.datasets.extend([sliced_stats.datasets[1]])
male_stats_name = sliced_stats.datasets[1].name

# Convert `Female` statistics (index=2) to the correct type and get the dataset name
female_stats_list = DatasetFeatureStatisticsList()
female_stats_list.datasets.extend([sliced_stats.datasets[2]])
female_stats_name = sliced_stats.datasets[2].name

# Visualize the two slices side by side
tfdv.visualize_statistics(
    lhs_statistics=male_stats_list,
    rhs_statistics=female_stats_list,
    lhs_name=male_stats_name,
    rhs_name=female_stats_name
)
```
