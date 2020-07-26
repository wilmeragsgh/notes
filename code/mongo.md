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