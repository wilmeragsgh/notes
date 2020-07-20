---
description: Frequently used ssh snippets
---

# SSH

## How to's

### Port forwarding

Say we want to connect to a web server running at `example.com:8080` and we have `user` to connect to the server. We can create a tunel to see the server on our local port `9000` by doing:

```bash
ssh -L 9000:localhost:8080 user@example.com
```

`localhost:8080`, is to forward connections from your local port `9000` to `localhost:8080` on your server. Now we can simply connect to our webserver.

### .pem managing

```bash
chmod 400 *.pem
```

### Add user

1. execute

   ```bash
   sudo adduser user
   ```

2. then, edit `/etc/ssh/sshd_config` and add/edit:

   ```bash
   AllowUsers user
   PasswordAuthentication yes
   ```

3. then, execute

```text
sudo service ssh reload
```

**Add to sudoers**

```text
usermod -aG sudo user
```

**Review ssh login attemps**

```bash
sudo vim /var/log/auth.log
```

**Copy the file "foobar.txt" from the local host to a remote host**

* ```bash
  scp foobar.txt your_username@remotehost.edu:/some/remote/directory
  ```

## References

* [Port forwarding](https://blog.trackets.com/2014/05/17/ssh-tunnel-local-and-remote-port-forwarding-explained-with-examples.html)

