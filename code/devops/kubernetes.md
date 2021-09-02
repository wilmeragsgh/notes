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

**Access a pod shell**

```bash
kubectl exec --stdin --tty POD_NAME -- /bin/bash
```

**Restart a deployment**

```bash
kubectl rollout restart deployments/DEPLOYMENT_NAME
```



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

### Services

**Connection**

- **Environment Variables**
  As soon as the Pod starts on any worker node, the **kubelet** daemon running on that node adds a set of environment variables in the Pod for all active Services. For example, if we have an active Service called **redis-master**, which exposes port **6379**, and its **ClusterIP** is **172.17.0.6**, then, on a newly created Pod, we can see the following environment variables:

- ***\*REDIS_MASTER_SERVICE_HOST=172.17.0.6\****
  ***\*REDIS_MASTER_SERVICE_PORT=6379\****
  ***\*REDIS_MASTER_PORT=tcp://172.17.0.6:6379\****
  ***\*REDIS_MASTER_PORT_6379_TCP=tcp://172.17.0.6:6379\****
  ***\*REDIS_MASTER_PORT_6379_TCP_PROTO=tcp\****
  ***\*REDIS_MASTER_PORT_6379_TCP_PORT=6379\****
  ***\*REDIS_MASTER_PORT_6379_TCP_ADDR=172.17.0.6\****

- With this solution, we need to be careful while ordering our Services, as the Pods will not have the environment variables set for Services which are created after the Pods are created.

- **DNS**
  Kubernetes has an add-on for **[DNS](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)**, which creates a DNS record for each Service and its format is **my-svc.my-namespace.svc.cluster.local**. Services within the same Namespace find other Services just by their names. If we add a Service **redis-master** in ***\*my-ns\**** Namespace, all Pods in the same **my-ns** Namespace lookup the Service just by its name, ***\*redis-master\****. Pods from other Namespaces, such as **test-ns**, lookup the same Service by adding the respective Namespace as a suffix, such as **redis-master.my-ns** or providing the **FQDN** of the service as **redis-master.my-ns.svc.cluster.local**. This is the most common and highly recommended solution. For example, in the previous section's image, we have seen that an internal DNS is configured, which maps our Services **frontend-svc** and ***\*db-svc\**** to **172.17.0.4** and **172.17.0.5** IP addresses respectively.

**ServiceType**

**ClusterIP** is the default ***[ServiceType](https://kubernetes.io/docs/concepts/services-networking/service/#nodeport)\***. A Service receives a Virtual IP address, known as its ClusterIP. This Virtual IP address is used for communicating with the Service and is accessible only from within the cluster.

With the **[NodePort](https://kubernetes.io/docs/concepts/services-networking/service/#nodeport)** **ServiceType**, in addition to a ClusterIP, a high-port, dynamically picked from the default range **30000-32767**, is mapped to the respective Service, from all the worker nodes. For example, if the mapped NodePort is **32233** for the service **frontend-svc**, then, if we connect to any worker node on port ***\*32233\****, the node would redirect all the traffic to the assigned ClusterIP - ***\*172.17.0.4\****. If we prefer a specific high-port number instead, then we can assign that high-port number to the NodePort from the default range when creating the Service.

The ***\*NodePort\**** *ServiceType* is useful when we want to make our Services accessible from the external world. The end-user connects to any worker node on the specified high-port, which proxies the request internally to the ClusterIP of the Service, then the request is forwarded to the applications running inside the cluster. Let's not forget that the Service is load balancing such requests, and only forwards the request to one of the Pods running the desired application. To manage access to multiple application Services from the external world, administrators can configure a reverse proxy - an ingress, and define rules that target specific Services within the cluster.

**LoadBalancer**

- NodePort and ClusterIP are automatically created, and the external load balancer will route to them
- The Service is exposed at a static port on each worker node
- The Service is exposed externally using the underlying cloud provider's load balancer feature.

The **LoadBalancer** *ServiceType* will only work if the underlying infrastructure supports the automatic creation of Load Balancers and have the respective support in Kubernetes, as is the case with the Google Cloud Platform and AWS. If no such feature is configured, the LoadBalancer IP address field is not populated, it remains in Pending state, but the Service will still work as a typical NodePort type Service.

### Sample manifests

**configMap**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: dev-env # parameter
data:
  APP_ENV: "DEV"
# ...
```

**secrets**

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: dev-password # parameter
type: Opaque
stringData:
  APP_SECRET_KEY: XYZZ
# ...
```

**deployment **

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: IMAGE_NAME
  labels:
    app: IMAGE_NAME
spec:
  selector:
    matchLabels:
      app: IMAGE_NAME
  replicas: 1
  template:
    metadata:
      labels:
        app: IMAGE_NAME
    spec:
      containers:
      - name: IMAGE_NAME
        image: DOCKER_HUB_USER/IMAGE_NAME:IMAGE_TAG # This needs to change over deployments to ensure update
        imagePullPolicy: Always
        ports:
          - containerPort: 8080
        resources:
          requests:
            cpu: "250m"
        envFrom:
          - configMapRef:
              name: dev-env # ^ from configMap
        env:
        - name: APP_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: dev-password # ^ from secrets
              key: APP_SECRET_KEY
```

**service**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: IMAGE_NAME-service
spec:
  selector:
    app: IMAGE_NAME
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```



### Storage

[references](https://kubernetes.io/docs/concepts/storage/volumes/)

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
- https://kubernetes.io/docs/concepts/services-networking/network-policies/
- https://artifacthub.io/
- https://github.com/helm/charts
- https://kubernetes.io/docs/concepts/workloads/controllers/job/
- https://kubernetes.io/docs/tasks/job/automated-tasks-with-cron-jobs/
- https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/apiserver-aggregation/
