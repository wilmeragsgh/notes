---
description: Jupyter knowledge and experiences
---

# Jupyter

## Recipes

**Installing - with docker**

```bash
docker run -it -p 8888:8888 -p 6006:6006 -d -v $(pwd)/notebooks:/notebooks amaksimov/python_data_science
```



## References

- https://dev-ops-notes.com/docker/howto-run-jupiter-keras-tensorflow-pandas-sklearn-and-matplotlib-docker-container/