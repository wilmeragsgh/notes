---
description: Frequently used bash snippets
---

# Bash

**Check access through ssh**

```bash
last | head
```

**Check open ports nmap**

```bash
while :; 
do nmap vpc-phishiq-es-gluq3jekytvcpv3xvesee65b7e.us-east-2.es.amazonaws.com -p443,9200,80,22 -Pn --max-rtt-timeout 60ms  ;
sleep 1 ; done
```

**Check open ports lsof**

```bash
sudo lsof -i -P -n #or
sudo lsof -i -P -n | grep LISTEN #or
lsof -i :8000 # by port
```

**Openning port in ubuntu**

```bash
sudo ufw allow [PORT]
```

**If statements**

```bash
if [ -z STRING]
then
fi
```

**If with multiple conditions and checking lenght == 0**

```bash
if [ -z $VAR1 ] || [ -z $VAR2]; then
# code
fi
```



**Kill processes**

```bash
kill -9 PID
```

**Search keywords in files within a directory**

```bash
grep -Hrn 'search term' path/to/files
```

**Remove character in-place with sed**

```bash
sed -i 's/past/future/g' file.txt
```

**Add character to the beginning of the file**

```bash
sed -i '1s/^/future/' file.txt
```

**Create sudo user**

```bash
adduser username
```

```bash
usermod -aG sudo username
```

**List omitting directory**

```bash
ls -1R -I [omit_dir]
```

**cURL requests**

```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"username":"xyz","password":"xyz"}' \
  http://localhost:3000/api/login
```

## tmux

**Create a new session**

```bash
tmux new -s sessionName
## Detached mode:
#tmux new -d -s sessionName
```

**List sessions**

```bash
tmux ls
```

**Attach a session**

```bash
tmux a -t sessionName
```

**Detach a session**

```text
C-a + d
```

**Send a command to a detached session**

```text
tmux send-keys -t sessionName.0 "echo 'Hello world'" ENTER
```

**Split panes for detached sessions**

```bash
tmux splitw -h -p 50 -t sessionName:1.0
# -p percentage of the display for the created pane
# -h or -v # horizontal/vertical splitting
## if we need to do it again we may need to select the pane we want to split first
tmux select-pane -t sessionName:1.0
tmux splitw -h -p 50 -t sessionName:1.0
```

**unzip file**

```bash
sudo apt install unzip #(ubuntu)
unzip target_file.zip
```

## References

* [https://dev.to/thiht/shell-scripts-matter](https://dev.to/thiht/shell-scripts-matter)
* [Awesome shell](https://github.com/alebcay/awesome-shell)

