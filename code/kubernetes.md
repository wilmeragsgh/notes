---
description: Frequently used code for kubernetes
---

# Kubernetes

## Recipes

**Installing kubectl**

```bash
sudo apt-get update && sudo apt-get install -y apt-transport-https gnupg2
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubectl
```

**Check version**

```bash
kubectl version --client
```

**Installing minikube**

```bash
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 \
  && chmod +x minikube

sudo install minikube /usr/local/bin/
```

*Installing KVM*

```bash
sudo apt-get install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils
```



## References

- https://kubernetes.io/docs/tasks/tools/install-minikube/
- https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-kubectl-on-linux
- https://help.ubuntu.com/community/KVM/Installation#Installation