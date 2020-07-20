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

## References:

* [PySpark ML and XGBoost full integration tested on the Kaggle Titanic dataset](https://towardsdatascience.com/pyspark-and-xgboost-integration-tested-on-the-kaggle-titanic-dataset-4e75a568bdb)
* [Building a Scalable Spark cluster with Docker Containers](https://towardsdatascience.com/building-a-scalable-spark-cluster-with-docker-containers-f921d860fa46)

