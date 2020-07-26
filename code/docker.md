---
description: Useful concepts and snippets for using Docker
---

# Docker



## Guidelines

- Always add *.dockerignore* file.
- Try to use and exploit multi-stage builds.



## Recipes

**Installing**

```bash
sudo apt-get update
curl -sSL https://get.docker.com/ | sh
sudo usermod -aG docker $USER
sudo service docker start
```

**Dockerfile With python venv's**

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

**Remove all exited containers:**
`docker rm $(docker ps -a -f status=exited -q)`

**Remove all images**
`docker rmi $(docker images -a -q)`



**Resources**

- https://pythonspeed.com/articles/multi-stage-docker-python/
- https://medium.com/capital-one-tech/multi-stage-builds-and-dockerfile-b5866d9e2f84
- https://pythonspeed.com/docker/
- [The Rabbit Hole of Using Docker in Automated Tests](http://gregoryszorc.com/blog/2014/10/16/the-rabbit-hole-of-using-docker-in-automated-tests/)
* [Bridget Kromhout](https://twitter.com/bridgetkromhout) has a useful blog post on [running Docker in production](http://sysadvent.blogspot.co.uk/2014/12/day-1-docker-in-production-reality-not.html) at Dramafever.
* There's also a best practices [blog post](http://developers.lyst.com/devops/2014/12/08/docker/) from Lyst.
* [Building a Development Environment With Docker](https://tersesystems.com/2013/11/20/building-a-development-environment-with-docker/)
* [Discourse in a Docker Container](https://samsaffron.com/archive/2013/11/07/discourse-in-a-docker-container)