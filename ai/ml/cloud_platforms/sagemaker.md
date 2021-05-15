---
description: Sagemaker related knowledge and experiances

---

# Sagemaker



## Installation

```bash
!pip install sagemaker==1.72.0 # This version was the one used for commands below
```



## Imports

```python
import sagemaker
from sagemaker import get_execution_role
from sagemaker.amazon.amazon_estimator import get_image_uri
from sagemaker.predictor import csv_serializer

# This is an object that represents the SageMaker session that we are currently operating in. This
# object contains some useful information that we will need to access later such as our region.
session = sagemaker.Session()

# This is an object that represents the IAM role that we are currently assigned. When we construct
# and launch the training job later we will need to tell it what IAM role it should have. Since our
# use case is relatively simple we will simply assign the training job the role we currently have.
role = get_execution_role()
```

## Uploading training data

Since we are currently running inside of a SageMaker session, we can use the object which represents this session to upload our data to the 'default' S3 bucket. Note that it is good practice to provide a custom prefix (essentially an S3 folder) to make sure that you don't accidentally interfere with data uploaded from some other notebook or project.

> header=False, index=False when uploading the data

```python
prefix = 'boston-xgboost-HL'

test_location = session.upload_data(os.path.join(data_dir, 'test.csv'), key_prefix=prefix)
val_location = session.upload_data(os.path.join(data_dir, 'validation.csv'), key_prefix=prefix)
train_location = session.upload_data(os.path.join(data_dir, 'train.csv'), key_prefix=prefix)
```

## Training model

Now that we have the training and validation data uploaded to S3, we can construct our XGBoost model and train it. We will be making use of the high level SageMaker API to do this which will make the resulting code a little easier to read at the cost of some flexibility.

To construct an estimator, the object which we wish to train, we need to provide the location of a container which contains the training code. Since we are using a built in algorithm this container is provided by Amazon. However, the full name of the container is a bit lengthy and depends on the region that we are operating in. Fortunately, SageMaker provides a useful utility method called `get_image_uri` that constructs the image name for us.

To use the `get_image_uri` method we need to provide it with our current region, which can be obtained from the session object, and the name of the algorithm we wish to use. In this notebook we will be using XGBoost however you could try another algorithm if you wish. The list of built in algorithms can be found in the list of [Common Parameters](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-algo-docker-registry-paths.html).

```python
# As stated above, we use this utility method to construct the image name for the training container.
container = sagemaker.image_uris.retrieve("xgboost", session.boto_region_name, "latest")

# Now that we know which container to use, we can construct the estimator object.
xgb = sagemaker.estimator.Estimator(container, # The image name of the training container
                                    role,      # The IAM role to use (our current role in this case)
                                    instance_count=1, # The number of instances to use for training
                                    instance_type='ml.m4.xlarge', # The type of instance to use for training
                                    output_path='s3://{}/{}/output'.format(session.default_bucket(), prefix),
                                                                        # Where to save the output (the model artifacts)
                                    sagemaker_session=session) # The current SageMaker session
```

## Hyperparameter setting

Before asking SageMaker to begin the training job, we should probably set any model specific hyperparameters. There are quite a few that can be set when using the XGBoost algorithm, below are just a few of them. If you would like to change the hyperparameters below or modify additional ones you can find additional information on the [XGBoost hyperparameter page](https://docs.aws.amazon.com/sagemaker/latest/dg/xgboost_hyperparameters.html)

```python
xgb.set_hyperparameters(max_depth=5,
                        eta=0.2,
                        gamma=4,
                        min_child_weight=6,
                        subsample=0.8,
                        objective='reg:linear', # 'binary:logistic' for classification
                        early_stopping_rounds=10,
                        num_round=500)
```

Now that we have our estimator object completely set up, it is time to train it. To do this we make sure that SageMaker knows our input data is in csv format and then execute the `fit` method.

## Training function call

```python
# This is a wrapper around the location of our train and validation data, to make sure that SageMaker
# knows our data is in csv format.
s3_input_train = sagemaker.s3_input(s3_data=train_location, content_type='csv')
s3_input_validation = sagemaker.s3_input(s3_data=val_location, content_type='csv')

xgb.fit({'train': s3_input_train, 'validation': s3_input_validation})

# xgb.wait()
```

## Testing the model

Now that we have fit our model to the training data, using the validation data to avoid overfitting, we can test our model. To do this we will make use of SageMaker's Batch Transform functionality. To start with, we need to build a transformer object from our fit model.

```python
xgb_transformer = xgb.transformer(instance_count=1, instance_type='ml.m4.xlarge')
```

### Data formatting

```python
train_x_np = train_features.astype("float32")
train_y_np = train_labels.astype("float32")

formatted_train_data = sagemaker_model.record_set(train_x_np, labels=train_y_np)
# sagemaker_model es la instancia que se ha creado para manejar el modelo
# labels could be empty in unsupervised cases
```



```python
xgb_transformer.transform(test_location, content_type='text/csv', split_type='Line')
```

Next we ask SageMaker to begin a batch transform job using our trained model and applying it to the test data we previously stored in S3. We need to make sure to provide SageMaker with the type of data that we are providing to our model, in our case `text/csv`, so that it knows how to serialize our data. In addition, we need to make sure to let SageMaker know how to split our data up into chunks if the entire data set happens to be too large to send to our model all at once.

Note that when we ask SageMaker to do this it will execute the batch transform job in the background. Since we need to wait for the results of this job before we can continue, we use the `wait()` method. An added benefit of this is that we get some output from our batch transform job which lets us know if anything went wrong.

```python
xgb_transformer.transform(test_location, content_type='text/csv', split_type='Line')
```

```python
xgb_transformer.wait()
```

Now that the batch transform job has finished, the resulting output is stored on S3. Since we wish to analyze the output inside of our notebook we can use a bit of notebook magic to copy the output file from its S3 location and save it locally.

```bash
!aws s3 cp --recursive $xgb_transformer.output_path $data_dir # in a sagemaker notebook, outside it would be different I guess.
```

To see how well our model works we can create a simple scatter plot between the predicted and actual values. If the model was completely accurate the resulting scatter plot would look like the line 𝑥=𝑦x=y. As we can see, our model seems to have done okay but there is room for improvement.

```python
Y_pred = pd.read_csv(os.path.join(data_dir, 'test.csv.out'), header=None)
```

## Sagemaker features

- **Notebook Instances** provide a convenient place to process and explore data in addition to making it very easy to interact with the rest of SageMaker's features.
- **Training Jobs** allow us to create *model artifacts* by fitting various machine learning models to data.
- **Hyperparameter Tuning** allow us to create multiple training jobs each with different hyperparameters in order to find the hyperparameters that work best for a given problem.
- **Models** are essentially a combination of *model artifacts* formed during a training job and an associated docker container (code) that is used to perform inference.
- **Endpoint Configurations** act as blueprints for endpoints. They describe what sort of resources should be used when an endpoint is constructed along with which models should be used and, if multiple models are to be used, how the incoming data should be split up among the various models.
- **Endpoints** are the actual HTTP URLs that are created by SageMaker and which have properties specified by their associated endpoint configurations. **Have you shut down your endpoints?**
- **Batch Transform** is the method by which you can perform inference on a whole bunch of data at once. In contrast, setting up an endpoint allows you to perform inference on small amounts of data by sending it do the endpoint bit by bit.



---

For model tuning review each sagemaker model documentation, for example, `LinealLearner` have a parameter called `binary_classifier_model_selection_criteria` that can be set to `precision_at_target_recall`, for example, passing `target_recall` as other parameter.



Also we can set a parameter for imbalance data: `positive_example_weight_mult='balanced'` along with selection criteria parameter above for example.



Optimization example:

> A bank has asked you to build a model that optimizes for a good user experience; users should only ever have up to about 15% of their valid transactions flagged as fraudulent.

*My thoughts*: If we're allowed about 15/100 incorrectly classified valid transactions (false positives), then I can calculate an approximate value for the precision that I want as: 85/(85+15) = 85%. I'll aim for about 5% higher during training to ensure that I get closer to 80-85% precision on the test data.

## References

- [What is](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)
- [Transformers](https://sagemaker.readthedocs.io/en/latest/transformer.html)
- [Estimators](https://sagemaker.readthedocs.io/en/latest/estimators.html)
- [Python SDK](https://sagemaker.readthedocs.io/en/latest/)
- [Built-in algorithms paths in Docker registry](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-algo-docker-registry-paths.html)
- [Xgboost in sagemaker](https://docs.aws.amazon.com/sagemaker/latest/dg/xgboost.html)
- [Model variants I](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_ProductionVariant.html)
- [Model variants II](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateEndpointConfig.html)
- https://github.com/udacity/sagemaker-deployment.git
- https://docs.aws.amazon.com/sagemaker/latest/dg/ex1-cleanup.html
- [Examples](https://github.com/awslabs/amazon-sagemaker-examples)
- [Pytorch Estimator](https://sagemaker.readthedocs.io/en/stable/sagemaker.pytorch.html#pytorch-model)
- 
