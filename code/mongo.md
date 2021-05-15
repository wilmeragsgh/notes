---
description: Frecuently used code for mongo
---

# Mongo

**Export database**:

```sh
mongodump --host <database-host> -d <database-name> --port <database-port> --out directory
```

**Import database**:

```sh
mongorestore --host <database-host> -d <database-name> --port <database-port> foldername
```

uri is also an option:

```sh
mongorestore --uri="uri" --dir="dir"
```



**Search by regex**

```js
db.collectionname.find({"name": {'$regex':'^File'}})
# All the documents that start with File
```



**Update field for a existing document**

```js
# Example
db.agents.find().forEach((doc) => {  doc.tags[0] = doc.tags[0].replace(">", "-"); db.agents.save(doc); });
```



## Python utils

**count records**

```python
collection.count_documents(query_string)
```



## Useful tools

- [restheart](https://restheart.org/)