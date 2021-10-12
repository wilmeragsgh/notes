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
# the line below can be used for selecting which columns we want to calculate metrics on
# stats_options = tfdv.StatsOptions(feature_whitelist=approved_cols)
train_stats = tfdv.generate_statistics_from_dataframe(train_df, stats_options)
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

# or complete substitution of a feature domain to the domain of another
tfdv.set_domain(schema, feature, to_domain_name)
```

**Manual set of range for int values**

```python
# Restrict the range of the `age` feature
tfdv.set_domain(schema, 'age', schema_pb2.IntDomain(name='age', min=17, max=90))

# Display the modified schema. Notice the `Domain` column of `age`.
tfdv.display_schema(schema)
```

**Data environments**

```python
schema.default_environment.append('TRAINING')
schema.default_environment.append('SERVING')

# If we want to remove a feature from a given environment (sample)
tfdv.get_feature(schema, 'readmitted').not_in_environment.append('SERVING')
```

**Data drift and skew**

```python
diabetes_med = tfdv.get_feature(schema, 'diabetesMed')
# domain knowledge helps to determine this threshold
diabetes_med.skew_comparator.infinity_norm.threshold = 0.03

skew_drift_anomalies = tfdv.validate_statistics(train_stats, schema,
                                          previous_statistics=eval_stats,
                                         serving_statistics=serving_stats)
tfdv.display_anomalies(skew_drift_anomalies)

```

**Freeze schema**

```python
schema_file = os.path.join(OUTPUT_DIR, 'schema.pbtxt')

# write_schema_text function expect the defined schema and output path as parameters
tfdv.write_schema_text(schema, schema_file)
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



**Generate tensorflow data directory**

```python
import os
import shutil
import csv

from sklearn.model_selection import train_test_split

def text_dataframe_to_tf_dir(df: pd.DataFrame, target_dir: str, label_col_ix: int = -1, value_col_ix: int = 0, train_split: float = 0.7, validation_split: float = 0.15, test_split: float = 0.15) -> None:
    """Generate a training data for tensorflow directory format

        The training data generated is meant to be loaded from tensorflow as follows:


        Args:
            (pd.DataFrame) df: Dataframe containing the text data for the model in the format of 'value\tlabel'.
            (str) target_dir: Target directory to place the formatted data.
            (int) label_col_ix: Label column to use for the directory generation.
            (int) value_col_ix: Value column to be written in the text files.
            (float) train_split: Percentage of data to be placed in the train subdir.
            (float) validation_split: Percentage of data to be placed in the valid subdir, only used if test_split and validation_split are not None.
            (float) test_split: Percentage of data to be placed in the test subdir.

        Returns:
            (None)

        Raises:
            IndexError: Column index for label column is out of columns boundaries.
    """
    try:
        label_col = df.columns[label_col_ix]
    except IndexError:
        raise IndexError(f'Column index "{label_col_ix}" is out of boundaries.')

    try:
        value_col = df.columns[value_col_ix]
    except IndexError:
        raise IndexError(f'Column index "{label_col_ix}" is out of boundaries.')

    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(target_dir)

    if train_split is not None:
        if test_split is not None:
            if validation_split is not None:
                val_test_split = validation_split + test_split
                train_set, test_set = train_test_split(df, test_size=val_test_split, random_state=42, stratify=df[label_col])
                validation_split = validation_split / val_test_split
                test_set, validation_set = train_test_split(test_set, test_size=validation_split, random_state=42, stratify=test_set[label_col])
                splits = [('train', train_set), ('test', test_set), ('validation', validation_set)]
            else:
                train_set, test_set = train_test_split(df, test_size=test_split, random_state=42, stratify=df[label_col])
                splits = [('train', train_set), ('test', test_set)]
        else:
            splits = [('train', df)]
    else:
        return


    for split_name, split_data in splits:
        print(f'Processing split "{split_name}"')
        split_dir = os.path.join(target_dir, split_name)
        os.makedirs(split_dir)
        for name, label_data in split_data.groupby(label_col):
            print(f'Processing label "{name}" for split {split_name}')
            label_dir = os.path.join(split_dir, str(name))
            os.makedirs(label_dir)
            for ix, obs in enumerate(label_data[value_col].tolist()):
                with open(os.path.join(label_dir, f'{name}_{ix}.txt'), 'w') as fl:
                    fl.write(obs)
```

The snippet above is meant to be loaded with [keras](https://www.tensorflow.org/api_docs/python/tf/keras/utils/text_dataset_from_directory) as follows:

```python
tf.keras.utils.text_dataset_from_directory(
    directory, labels='inferred', label_mode='int',
    class_names=None, batch_size=32, max_length=None, shuffle=True, seed=None,
    validation_split=None, subset=None, follow_links=False
)
```

**Feature preprocessing**

Metadata definition

```python
import tensorflow as tf
from tensorflow_transform.tf_metadata import dataset_metadata
from tensorflow_transform.tf_metadata import schema_utils

# define the schema as a DatasetMetadata object
raw_data_metadata = dataset_metadata.DatasetMetadata(
    
    # use convenience function to build a Schema protobuf
    schema_utils.schema_from_feature_spec({
        
        # define a dictionary mapping the keys to its feature spec type
        'y': tf.io.FixedLenFeature([], tf.float32),
        'x': tf.io.FixedLenFeature([], tf.float32),
        's': tf.io.FixedLenFeature([], tf.string),
    }))
```

Sample preprocessing function

```python
def preprocessing_fn(inputs):
    """Preprocess input columns into transformed columns."""
    
    # extract the columns and assign to local variables
    x = inputs['x']
    y = inputs['y']
    s = inputs['s']
    
    # data transformations using tft functions
    x_centered = x - tft.mean(x)
    y_normalized = tft.scale_to_0_1(y)
    s_integerized = tft.compute_and_apply_vocabulary(s)
    x_centered_times_y_normalized = (x_centered * y_normalized)
    
    # return the transformed data
    return {
        'x_centered': x_centered,
        'y_normalized': y_normalized,
        's_integerized': s_integerized,
        'x_centered_times_y_normalized': x_centered_times_y_normalized,
    }
```

Generate a constant graph with the required transformations

```python
# Ignore the warnings
tf.get_logger().setLevel('ERROR')

# a temporary directory is needed when analyzing the data
with tft_beam.Context(temp_dir=tempfile.mkdtemp()):
    
    # define the pipeline using Apache Beam syntax
    transformed_dataset, transform_fn = (
        
        # analyze and transform the dataset using the preprocessing function
        (raw_data, raw_data_metadata) | tft_beam.AnalyzeAndTransformDataset(
            preprocessing_fn)
    )

# unpack the transformed dataset
transformed_data, transformed_metadata = transformed_dataset
```

**Run tf pipeline**

```python
# Initialize the InteractiveContext with a local sqlite file.
# If you leave `_pipeline_root` blank, then the db will be created in a temporary directory.
from tfx.orchestration.experimental.interactive.interactive_context import InteractiveContext

context = InteractiveContext(pipeline_root=_pipeline_root)
```

read csv file 

`_data_root` can be csv, tf.Record and BigQuery.

```python
from tfx.components import CsvExampleGen

# Instantiate ExampleGen with the input CSV dataset
example_gen = CsvExampleGen(input_base=_data_root)
context.run(example_gen)
```

Inspect generated artifact

It will keep each run associated with an ID for that execution for debugging

```python
# get the artifact object
artifact = example_gen.outputs['examples'].get()[0]

# print split names and uri
print(f'split names: {artifact.split_names}')
print(f'artifact uri: {artifact.uri}')
```

**Read and print tf.Record files**

```python
train_uri = os.path.join(artifact.uri, 'train')

# Get the list of files in this directory (all compressed TFRecord files)
tfrecord_filenames = [os.path.join(train_uri, name)
                      for name in os.listdir(train_uri)]

# Create a `TFRecordDataset` to read these files
dataset = tf.data.TFRecordDataset(tfrecord_filenames, compression_type="GZIP")
```

```python
from google.protobuf.json_format import MessageToDict

def get_records(dataset, num_records):
    '''Extracts records from the given dataset.
    Args:
        dataset (TFRecordDataset): dataset saved by ExampleGen
        num_records (int): number of records to preview
    '''
    
    # initialize an empty list
    records = []
    
    # Use the `take()` method to specify how many records to get
    for tfrecord in dataset.take(num_records):
        
        # Get the numpy property of the tensor
        serialized_example = tfrecord.numpy()
        
        # Initialize a `tf.train.Example()` to read the serialized data
        example = tf.train.Example()
        
        # Read the example data (output is a protocol buffer message)
        example.ParseFromString(serialized_example)
        
        # convert the protocol buffer message to a Python dictionary
        example_dict = (MessageToDict(example))
        
        # append to the records list
        records.append(example_dict)
        
    return records
```

Sample usage

```python
import pprint
pp = pprint.PrettyPrinter()

# Get 3 records from the dataset
sample_records = get_records(dataset, 3)

# Print the output
pp.pprint(sample_records)
```

**Generate statistics for a given dataset**

```python
from tfx.components import StatisticsGen

# Instantiate StatisticsGen with the ExampleGen ingested dataset
statistics_gen = StatisticsGen(
    examples=example_gen.outputs['examples'])
# example_gen from above

# Execute the component
context.run(statistics_gen)
```

Show the statistics

```python
context.show(statistics_gen.outputs['statistics'])
```

**Infer schema for a given dataset**

```python
from tfx.components import SchemaGen
# Instantiate SchemaGen with the StatisticsGen ingested dataset
schema_gen = SchemaGen(
    statistics=statistics_gen.outputs['statistics'],
    )

# Run the component
context.run(schema_gen)
```

Show schema

```python
context.show(schema_gen.outputs['schema'])
```

**Detect anomalies for a given dataset**

```python
# Instantiate ExampleValidator with the StatisticsGen and SchemaGen ingested data
example_validator = ExampleValidator(
    statistics=statistics_gen.outputs['statistics'],
    schema=schema_gen.outputs['schema'])

# Run the component.
context.run(example_validator)
```

Show anomalies (if any)

```python
context.show(example_validator.outputs['anomalies'])
```

**Apply transformations to a given dataset**

Transformations need to be passed as modules to tfx a common pattern is to have a constant file as follows

```python
# Features with string data types that will be converted to indices
CATEGORICAL_FEATURE_KEYS = [
    'education', 'marital-status', 'occupation', 'race', 'relationship', 'workclass', 'sex', 'native-country'
]

# Numerical features that are marked as continuous
NUMERIC_FEATURE_KEYS = ['fnlwgt', 'education-num', 'capital-gain', 'capital-loss', 'hours-per-week']

# Feature that can be grouped into buckets
BUCKET_FEATURE_KEYS = ['age']

# Number of buckets used by tf.transform for encoding each bucket feature.
FEATURE_BUCKET_COUNT = {'age': 4}

# Feature that the model will predict
LABEL_KEY = 'label'

# Utility function for renaming the feature
def transformed_name(key):
    return key + '_xf'
```

Then, having the following sample processing function in a file

`_census_transform_module_file = 'census_transform.py'`

```python
import tensorflow as tf
import tensorflow_transform as tft

import census_constants # this is the constants file from above

# Unpack the contents of the constants module
_NUMERIC_FEATURE_KEYS = census_constants.NUMERIC_FEATURE_KEYS
_CATEGORICAL_FEATURE_KEYS = census_constants.CATEGORICAL_FEATURE_KEYS
_BUCKET_FEATURE_KEYS = census_constants.BUCKET_FEATURE_KEYS
_FEATURE_BUCKET_COUNT = census_constants.FEATURE_BUCKET_COUNT
_LABEL_KEY = census_constants.LABEL_KEY
_transformed_name = census_constants.transformed_name


# Define the transformations
def preprocessing_fn(inputs):
    """tf.transform's callback function for preprocessing inputs.
    Args:
        inputs: map from feature keys to raw not-yet-transformed features.
    Returns:
        Map from string feature key to transformed feature operations.
    """
    outputs = {}

    # Scale these features to the range [0,1]
    for key in _NUMERIC_FEATURE_KEYS:
        outputs[_transformed_name(key)] = tft.scale_to_0_1(
            inputs[key])
    
    # Bucketize these features
    for key in _BUCKET_FEATURE_KEYS:
        outputs[_transformed_name(key)] = tft.bucketize(
            inputs[key], _FEATURE_BUCKET_COUNT[key],
            always_return_num_quantiles=False)

    # Convert strings to indices in a vocabulary
    for key in _CATEGORICAL_FEATURE_KEYS:
        outputs[_transformed_name(key)] = tft.compute_and_apply_vocabulary(inputs[key])

    # Convert the label strings to an index
    outputs[_transformed_name(_LABEL_KEY)] = tft.compute_and_apply_vocabulary(inputs[_LABEL_KEY])

    return outputs
```

we will pass it to the transform function as follows:

```python
from tfx.components import Transform

# Ignore TF warning messages
tf.get_logger().setLevel('ERROR')

# Instantiate the Transform component
transform = Transform(
    examples=example_gen.outputs['examples'],
    schema=schema_gen.outputs['schema'],
    module_file=os.path.abspath(_census_transform_module_file))



# Run the component
context.run(transform)
```

This execution will produce (in `.component.outputs`):

* `transform_graph` is the graph that can perform the preprocessing operations. This graph will be included during training and serving to ensure consistent transformations of incoming data.
* `transformed_examples` points to the preprocessed training and evaluation data.
* `updated_analyzer_cache` are stored calculations from previous runs.



`transform_graph` for example would have (in `transform.outputs['transform_graph'].get()[0].uri`):

* The `metadata` subdirectory contains the schema of the original data.
* The `transformed_metadata` subdirectory contains the schema of the preprocessed data. 
* The `transform_fn` subdirectory contains the actual preprocessing graph. 

A sample of transformed data can be retrieved with

```python
train_uri = os.path.join(transform.outputs['transformed_examples'].get()[0].uri, 'train')

# Get the list of files in this directory (all compressed TFRecord files)
tfrecord_filenames = [os.path.join(train_uri, name)
                      for name in os.listdir(train_uri)]

# Create a `TFRecordDataset` to read these files
transformed_dataset = tf.data.TFRecordDataset(tfrecord_filenames, compression_type="GZIP")

# Get 3 records from the dataset
sample_records_xf = get_records(transformed_dataset, 3)

# Print the output
pp.pprint(sample_records_xf)
```



**References**

- https://www.tensorflow.org/api_docs/python/tf/
