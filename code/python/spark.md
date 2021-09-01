---
description: Frequently used code for spark related code snippets
---

# Spark

**Create Spark session:**

```python
#!pip install pyspark
#!pip install findspark

#import os
#os.environ["SPARK_HOME"] = "/opt/spark-3.0.0" # might be required
#import findspark
findspark.init()
from pyspark.sql import SparkSession
spark = SparkSession.builder \
    .master("local[*]") \
    .appName("Learning_Spark") \
    .getOrCreate()
sc = spark.sparkContext # Sometimes required
```

**Create dataframe from json:**

```python
import json
jsonStrings = [json.dumps(x, ensure_ascii=False) for x in json_array]
otherPeopleRDD = sc.parallelize(jsonStrings)
otherPeople = spark.read.json(otherPeopleRDD)
otherPeople.show()
```

**Concatenate dataframe**

```python
result = df_1.union(df_2)
#result.show()
```

**Print schema**

```python
df.printSchema()
```

**Select columns**

```python
df.select(['colname'])
```

**Create new columns**

```python
df.withColumns('new_col',col_value)
```

**Print dataframe**

```python
df.show()
```

**Apply SQL to dataframe**

```python
df.createOrReplaceTempView("associates") #Creating a view called associates
sql_result_1 = spark.sql("SELECT * FROM associates") #Applying SQL query on associates
print("Showing the results of the select query")
sql_result_1.show()
```

**Filter rows**

```python
df.filter("total_amount > 1000").collect()
# or df.filter(df["total_amount"] > 1000).collect()
```

**Transform to dict**

```python
result_data[0].asDict()
```

**Group by**

```python
df.groupBy("colname").sum().show()
# alternative to sum:
# count()
# mean()
# max()
# min()
# sum()
# avg()
# agg()
# agg({"revenue_sales":"max"}) it's also valid
# order:
# orderBy("revenue_sales")
```

**Example classification**

```python
from pyspark.ml.feature import VectorAssembler,VectorIndexer,StringIndexer,OneHotEncoder
#Formatting the categorical column - sex
#Creating a String Indexer - To convert every string into a unique number
sex_string_indexer_direct = StringIndexer(inputCol='sex',outputCol='sexIndexer')
indexed_data = sex_string_indexer_direct.fit(data)
final_string_indexed_data = indexed_data.transform(data)
# Male - 1 and Female 0 or vice versa
#Performing OneHotEncoing - convert this value into an array form
sex_encoder_direct = OneHotEncoder(inputCol='sexIndexer',outputCol='sexVector')
encoded_data = sex_encoder_direct.transform(final_string_indexed_data)
# Male - [1,0] and Female - [0,1] or vice versa
print("Data after OneHotEncoding")
encoded_data.show(4)
assembler_direct = VectorAssembler(inputCols=['age','sexVector','tumor_size'],outputCol='features')
assembler_data = assembler_direct.transform(encoded_data)
final_data_direct = assembler_data.select('features','cancerous')
print("Consolidated Data with accepted features and labels")
final_data_direct.show(3)
#Step 3 - Training our Logistic Regression model
from pyspark.ml.classification import LogisticRegression
logreg_direct = LogisticRegression(featuresCol='features',labelCol='cancerous')
train_data_direct,test_data_direct = final_data_direct.randomSplit([0.6,0.4])
logreg_model_direct = logreg_direct.fit(train_data_direct)
#Step 4 - Evaluating and performing Predictions on our model
#Evaluating our model with testing data
#Direct Evaluation using Trivial method
predictions_labels = logreg_model_direct.evaluate(test_data_direct)
print("Prediction Data")
predictions_labels.predictions.select(['features','cancerous',
'prediction']).show(3)

#Evaluation using BinaryClassificationEvaluator
from pyspark.ml.evaluation import BinaryClassificationEvaluator
direct_evaluation = BinaryClassificationEvaluator(rawPredictionCol='prediction',labelCol='cancerous')
AUC_direct = direct_evaluation.evaluate(predictions_labels.predictions)
print("Area Under the Curve value is {}".format(AUC_direct))
print("\nCoeffecients are {}".format(logreg_model_direct.coefficients))
print("\nIntercept is {}".format(logreg_model_direct.intercept))
```

### NLP tools

**Tokenization**

```python
from pyspark.ml.feature import Tokenizer,RegexTokenizer
#Applying Tokenizer class which splits text on whitespaces
simple_tokenizer = Tokenizer(inputCol='text_content',outputCol='tokens_words')
simple_tokens = simple_tokenizer.transform(data)
print("Tokenizer Output - Splitting text on Whitespaces")
simple_tokens.show(truncate=False)

#Applying RegexTokenizer class which splits text on user defined patterns
# Special sequence \W splits on non-alphanumeric characters (in our case it splits on '-')
regex_tokenizer = RegexTokenizer(inputCol='text_content',outputCol='tokens_words',pattern='\\W')
regex_tokens = regex_tokenizer.transform(data)
print("RegexTokenizer Output - Splitting text on special sequence \W")
regex_tokens.show(truncate=False)
```

**Stop words**

```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('StopWordsRemover').getOrCreate()
from pyspark.ml.feature import StopWordsRemover, Tokenizer
data = spark.read.csv('stopwords.csv',header=True,inferSchema=True)
print("Initial Data")
data.show(truncate=False)
#Applying Tokenizer prior to StopWordsRemover as StopWords takes tokens as its input
simple_tokenizer = Tokenizer(inputCol='text_content',outputCol='tokens_words')
simple_tokens = simple_tokenizer.transform(data)
print("Tokenizer Output - Splitting text on Whitespaces")
simple_tokens.show(truncate=False)
#Applying StopWordsRemover class
stopWords = StopWordsRemover(inputCol='tokens_words',outputCol='stopWordsRemoved')
stopWords_tokens = stopWords.transform(simple_tokens)
print("Data after Stop Words Removal")
stopWords_tokens.select('tokens_words','stopWordsRemoved').show(truncate=False)
```

**TFIDF**

```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('TFIDF_HashTF').getOrCreate()

from pyspark.ml.feature import Tokenizer,HashingTF,IDF
data = spark.read.csv('reviews_tfidf.csv',header=True,inferSchema=True)
print("Initial Data")
data.show(truncate=False)
#Applying Tokenizer class which splits text on whitespaces
simple_tokenizer = Tokenizer(inputCol='reviews',outputCol='review_tokens')
simple_tokens = simple_tokenizer.transform(data)
print("Tokenizer Output - Splitting text on Whitespaces")
simple_tokens.show(truncate=False)
#Applying HashingTF
hashingtf_vectors = HashingTF(inputCol='review_tokens',outputCol='hashVec')
HashingTF_featurized_data = hashingtf_vectors.transform(simple_tokens)
print("HashingTF Data")
HashingTF_featurized_data.select('review_tokens','hashVec').show(truncate=40)
#Applying CountVectorizer to convert tokens to vectors of token count
# count_vectors = CountVectorizer(inputCol='review_tokens',outputCol='countVec')
# count_vectors_model = count_vectors.fit(simple_tokens)
# countVector_featurized_data = count_vectors_model.transform(simple_tokens)
# print("CountVectorizer Data")
# countVector_featurized_data.select('review_tokens','countVec').show(truncate=False)

#Applying IDF on vectors of token count output from HashingTF
idf = IDF(inputCol='hashVec',outputCol='features')
idf_model = idf.fit(HashingTF_featurized_data)
final_data = idf_model.transform(HashingTF_featurized_data)
print("Final Spark accepted Data - NLP Formatted Data ready to pass into any Machine Learning Model")
final_data.select('label','features').show(truncate=60)
```

## References:

* [PySpark ML and XGBoost full integration tested on the Kaggle Titanic dataset](https://towardsdatascience.com/pyspark-and-xgboost-integration-tested-on-the-kaggle-titanic-dataset-4e75a568bdb)
* [Building a Scalable Spark cluster with Docker Containers](https://towardsdatascience.com/building-a-scalable-spark-cluster-with-docker-containers-f921d860fa46)

