---
description: Elasticsearch knowledge and experiences
---

# Elasticsearch

## Recipes

**Inserting to an index**

```python
from elasticsearch import Elasticsearch
from elasticsearch.herlpers import bulk

es = Elasticsearch([ENDPOINT])

# ====== Inserting Documents ====== #
# Creating a simple Pandas DataFrame
liste_hello = ['hello1','hello2']
liste_world = ['world1','world2']
df = pd.DataFrame(data = {'hello' : liste_hello, 'world': liste_world})
 
# Bulk inserting documents. Each row in the DataFrame will be a document in ElasticSearch
documents = df.to_dict(orient='records')
bulk(es, documents, index='helloworld',doc_type='foo', raise_on_error=True)
```

**Searching on an index**

```python
# ====== Searching Documents ====== #
# Retrieving all documents in index (no query given)
documents = es.search(index='helloworld',body={})['hits']['hits']
df = pd.DataFrame(documents)
 
# Retrieving documents in index that match a query
documents2 = es.search(index='helloworld',body={"query":{"term":{"hello" : "hello1" }}})['hits']['hits']
df2 = pd.DataFrame(documents2)

```

**Try this for analyzers**

```python
res= es.search(index="test-index", doc_type='content-field',body={"query": {"match": {"text": {"query": "微观文明", "analyzer": "ik_smart"}}}})
```

**Dumping data for a query**

```bash
elasticdump \
  --input=server_url/db_name \
  --output=tags_0.json \
  --searchBody='{"query":{"term":{"tag": 0}}}'
```

**Dumping data for Mappings**

```bash
elasticdump \
  --input=server_url/apirequests \
  --output=/data/apirequests_mapping.json \
  --type=mapping
```
**Dumping data for Data**

```bash
elasticdump \
  --input=server_url/apirequests \
  --output=apirequests_data.json \
  --type=data
```

**Scrolling over cursor**

Example with urls as data

```python
filter = {
  "query": {
    "match": {
          "tag": 0
    }
  }
}

results = es.search(index='index_name', doc_type='doc_type', body=filter,scroll='2m',size=1000)
# Get the scroll ID
sid = results['_scroll_id']
scroll_size = results['hits']['total']
# Before scroll, process current batch of hits
results_dt = pd.concat(map(pd.DataFrame.from_dict, results['hits']['hits']), axis=1)['_source'].T
results_dt = results_dt.reset_index(drop=True)
while scroll_size > 0:
    results = es.scroll(scroll_id=sid, scroll='2m')
    print(results_dt.shape)
    results_dt_temp = pd.concat(map(pd.DataFrame.from_dict, results['hits']['hits']), axis=1)['_source'].T
    results_dt_temp = results_dt_temp.reset_index(drop=True)
    results_dt = pd.concat([results_dt, results_dt_temp],axis=0)
    # Update the scroll ID
    sid = results['_scroll_id']
    # Get the number of results that returned in the last scroll
    scroll_size = len(results['hits']['hits'])
```