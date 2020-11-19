---
description: Thoughts and snippets related to Linux

---

# Linux

Here there are going to be some Snippets from my experience with Linux as apps, practices and getting started steps I might use across Linux installations.



## Apps

### Non-officials

- https://ulauncher.io/

### Officials

**terminator**

```bash
sudo add-apt-repository ppa:gnome-terminator

sudo apt-get update

sudo apt-get install terminator
```

**slack**

https://slack.com/intl/en-ve/downloads/linux



**Typora** (https://typora.io/)

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

https://go.microsoft.com/fwlink/?LinkID=760868