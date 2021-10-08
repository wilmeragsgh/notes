---
description: Thoughts and snippets related to Linux
---

# Linux

Here there are going to be some Snippets from my experience with Linux as apps, practices and getting started steps I might use across Linux installations.

## Distros

* Elementary
* Xubuntu
* Arch
* Ubuntu

## Apps

### Non-officials

* [https://ulauncher.io/](https://ulauncher.io/)

### Officials

**terminator**

```bash
sudo add-apt-repository ppa:gnome-terminator

sudo apt-get update

sudo apt-get install terminator
```

**slack**

[https://slack.com/intl/en-ve/downloads/linux](https://slack.com/intl/en-ve/downloads/linux)

**Typora** \([https://typora.io/](https://typora.io/)\)

```bash
# or use
# sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys BA300B7755AFCFAE
wget -qO - https://typora.io/linux/public-key.asc | sudo apt-key add -

# add Typora's repository
sudo add-apt-repository 'deb https://typora.io/linux ./'
sudo apt-get update

# install typora
sudo apt-get install typora
```

**vim**

`sudo apt install vim`

**vscode**

[https://go.microsoft.com/fwlink/?LinkID=760868](https://go.microsoft.com/fwlink/?LinkID=760868)

### Others

* chrome
* authy
* [bitwarden](https://bitwarden.com/download/)
* calibre
* keybase
* [kite](https://www.kite.com/download/)
* compass
* notejot
* Rstudio
* Postman
* R
* [Docker](https://github.com/wilmeragsgh/notes/tree/29e7ea4d8d58253cead34ada44c21a4ad9f66177/linux/code/docker.md)
* shutdown scheduler
* torrential
* [terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
* [aws-cli](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html)
* xournal
* [zoom](https://zoom.us/download?os=linux)
* [datashare](https://datashare.icij.org/)

### Web tools

[outline](https://www.getoutline.com/)

[https://n8n.io/](https://n8n.io/)

[https://strapi.io/](https://strapi.io/)

## Commands

**Add/Remove ppa**

```bash
sudo add-apt-repository ppa:name/here
# --remove flag for removing
```



## Resources

- https://github.com/yudai/gotty
- https://github.com/stitchfix/flotilla-os
