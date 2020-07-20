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

* `tf.sigmoid`
* `tf.nn.sigmoid_cross_entropy_with_logits` 
* `tf.ones`
* `tf.zeros_initializer`
* `tf.contrib.layers.xavier_initializer(seed = 1)`
* `tf.nn.relu`
* `tf.add`
* `tf.matmul`
* `tf.transpose`

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

