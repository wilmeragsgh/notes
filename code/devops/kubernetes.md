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

**Create namespace**

```bash
kubectl create namespace twitter-executor
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



**Set new image for a given deployment**

```bash
kubectl set image deploy DEPLOYMENT_NAME IMAGENAME=IMAGENAME:ERSION
```

**Get revisions**

```bash
kubectl get rs -n NAMESPACE
```

**Rollback to previous revision**

```bash
kubectl rollout undo deployment DEPLOYMENT_NAME --to-revision=REVISION_NUMBER	
```

**Inspect revisions**

```bash
kubectl rollout history deploy DEPLOYNAME -n NAMESPACE --revision=REVISION_NUMBER
```

> Revisions used for rollback are available as their new revision instead of their original.



![image-20210702225147344](/home/w/.config/Typora/typora-user-images/image-20210702225147344.png)



![image-20210702225306182](/home/w/.config/Typora/typora-user-images/image-20210702225306182.png)

> That's what the selector field in the service manifest is for

**Scale deployment**

```bash
kubectl scale deployment tasksapp --replicas=3
```

**Set namespace**

```bash
kubectl config set-context --current --namespace=dev
```



## Resources

- https://keda.sh/
- https://www.bodyworkml.com/
- https://github.com/CrunchyData/postgres-operator

## References

- https://kubernetes.io/docs/tasks/tools/install-minikube/
- https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-kubectl-on-linux
- https://minikube.sigs.k8s.io/docs/start/
- https://help.ubuntu.com/community/KVM/Installation#Installation
- https://minikube.sigs.k8s.io/docs/handbook/accessing/#using-minikube-tunnel
- https://levelup.gitconnected.com/deploy-your-first-flask-mongodb-app-on-kubernetes-8f5a33fa43b4
- https://github.com/testdrivenio/flask-vue-kubernetes !! Useful
