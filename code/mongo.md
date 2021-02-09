---
description: Frecuently used code for mongo
---

# Mongo

**Export database**:

```sh
mongodump -d <database_name> -o <directory_backup>
```

**Import database**:

```sh
mongorestore -d <database_name> <directory_backup>
```

**Search by regex**

```js
db.collectionname.find({"name": {'$regex':'^File'}})
# All the documents that start with File
```



## Useful tools

- [restheart](https://restheart.org/)