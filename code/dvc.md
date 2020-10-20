---
description: Useful concepts and snippets for using dvc

---

# 

# dvc



**Add new changes**

```bash
dvc commit # on a dvc init repo
```

**Add ssh remote storage**

```bash
dvc remote add -d NAMEREMOTE ssh://USER@SERVER/PATH
dvc remote modify NAMEREMOTE keyfile PATH/TO/.pem
# dvc push
# dvc pull
```



