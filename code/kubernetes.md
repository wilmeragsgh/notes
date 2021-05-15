---
description: Frequently used code for kubernetes
---

# Kubernetes

## Recipes

**Installing kubectl**

(dependencies):

```bash
sudo apt-get update && sudo apt-get install -y apt-transport-https gnupg2
```

```bash
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg

echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt-get update
sudo apt-get install -y kubectl
```

**Check version**

```bash
kubectl version --client
```

**Installing minikube**

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube_latest_amd64.deb
sudo dpkg -i minikube_latest_amd64.deb

```

*Installing KVM*

```bash
sudo apt-get install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils
```

**Installing helm**

```bash
curl https://baltocdn.com/helm/signing.asc | sudo apt-key add -
sudo apt-get install apt-transport-https --yes
echo "deb https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```



**Start cluster**

```shell
minikube start
```

**Delete namespace**

```bash
kubectl delete namespace <name-of-the-namespace>
```



**To run a service from minikube**

`minikube service <name-of-the-service> -n <name-of-the-namespace>`

for example for jupyterhub: `minikube service proxy-public -n jhub`



**To inspect running cluster**

`minikube dashboard`



**Applying conf changes**

1. Change config.yaml

2. Execute `helm upgrade` as follows:

   ```bash
   # In some cases to guarantee upgrade:
   # These two need to be run every time config.yaml is updated it
   # helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
   # helm repo update
   RELEASE=jhub
   NAMESPACE=jhub
   helm upgrade --cleanup-on-fail \
     $RELEASE jupyterhub/jupyterhub \
     --namespace $NAMESPACE \
     --version=0.10.6 \
     --values config.yaml # --timeout 2000s if internet slow
   ```

3. Verify hub and proxy pods:

   ```bash
   NAMESPACE=jhub
   kubectl get pod --namespace $NAMESPACE
   ```


## References

- https://kubernetes.io/docs/tasks/tools/install-minikube/
- https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-kubectl-on-linux
- https://minikube.sigs.k8s.io/docs/start/
- https://help.ubuntu.com/community/KVM/Installation#Installation
