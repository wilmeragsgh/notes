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
mongorestore -d <database_name> <directory_backup>
```

**Search by regex**

```js
db.collectionname.find({"name": {'$regex':'^File'}})
# All the documents that start with File
```



## Useful tools

- [restheart](https://restheart.org/)