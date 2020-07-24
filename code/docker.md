---
description: Useful concepts and snippets for using Docker

---

# Docker



## Guidelines

- Always add *.dockerignore* file.
- Try to use and exploit multi-stage builds.



## How-to

### Install

```bash
sudo apt-get update
curl -sSL https://get.docker.com/ | sh
sudo usermod -aG docker $USER
sudo service docker start
```





## Examples

**With python venv's**

```dockerfile
FROM python:3.8-slim-buster

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

# Run the application:
COPY myapp.py .
CMD ["python", "myapp.py"]
```



**Resources**

- https://pythonspeed.com/articles/multi-stage-docker-python/
- https://medium.com/capital-one-tech/multi-stage-builds-and-dockerfile-b5866d9e2f84
- https://pythonspeed.com/docker/