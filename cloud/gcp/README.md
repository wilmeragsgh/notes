# Google Cloud platform snippets


## Create GKE cluster
> From cloud shell


```bash
gcloud config set compute/zone us-central1-f
PROJECT_ID=$(gcloud config get-value project)
CLUSTER_NAME=cluster-1
```

```bash
gcloud container clusters create $CLUSTER_NAME \
  --project=$PROJECT_ID \
  --release-channel=stable \
  --machine-type=n1-standard-4 \
  --scopes compute-rw,gke-default,storage-rw \
  --num-nodes=3
```

```bash
gcloud container clusters get-credentials $CLUSTER_NAME
```


## Deploy `TFJob` components

[TFJob](https://www.kubeflow.org/docs/components/training/tftraining/) is a component of [Kubeflow](https://www.kubeflow.org/). It is usually deployed as part of a full **Kubeflow** installation but can also be used in a standalone configuration. In this lab, you will install **TFJob** as a standalone component.

**TFJob** consists of two parts: a Kubernetes [custom resource](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) and an [operator](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) implementing the job management logic. Kubernetes manifests for both the custom resource definition and the operator are managed in **Kubeflow GitHub** repository.

Instead of cloning the whole repository you will retrieve the **TFJob** manifests only using an OSS tool - [kpt](https://googlecontainertools.github.io/kpt/) - that is pre-installed in **Cloud Shell**.

```bash
cd
SRC_REPO=https://github.com/kubeflow/manifests
kpt pkg get $SRC_REPO/tf-training@v1.1.0 tf-training
```

```bash
kubectl create namespace kubeflow
```

```bash
kubectl apply  --kustomize tf-training/tf-job-crds/base
```

```bash
kubectl apply  --kustomize tf-training/tf-job-operator/base
```

> Verify instalation

```bash
kubectl get deployments -n kubeflow
```

### Preparing TFJob
Your distributed training environment is ready and you can now prepare and submit distributed training jobs.

The TensorFlow training code and the **TFJob** manifest template used in the lab can be retrieved from **GitHub**.

```bash
cd
SRC_REPO=https://github.com/GoogleCloudPlatform/mlops-on-gcp
kpt pkg get $SRC_REPO/workshops/mlep-qwiklabs/distributed-training-gke lab-files
cd lab-files

```

The training module is in the `mnist` folder. The `model.py` file contains a function to create a simple convolutional network. The `main.py` file contains data preprocessing routines and a distributed training loop. Review the files. Notice how you can use a `tf.distribute.experimental.MultiWorkerMirrorStrategy()` object to retrieve information about the topology of the distributed cluster running a job.


#### Packaging training code in a docker image

Before submitting the job, the training code must be packaged in a docker image and pushed into your project's [Container Registry](https://cloud.google.com/container-registry). You can find the Dockerfile that creates the image in the `lab-files` folder. You do not need to modify the Dockerfile.

To build the image and push it to the registry execute the below commands

```bash
IMAGE_NAME=mnist-train
docker build -t gcr.io/${PROJECT_ID}/${IMAGE_NAME} .
docker push gcr.io/${PROJECT_ID}/${IMAGE_NAME}
```

#### Updating the TFJob manifest

_sample_
```yaml
apiVersion: kubeflow.org/v1
kind: TFJob
metadata:
  name: multi-worker
spec:
  cleanPodPolicy: None
  tfReplicaSpecs:
    Worker:
      replicas: 3
      template:
        spec:
          containers:
            - name: tensorflow
              image: mnist
              args:
                - --epochs=5
                - --steps_per_epoch=100
                - --per_worker_batch=64
                - --saved_model_path=gs://bucket/saved_model_dir
                - --checkpoint_path=gs://bucket/checkpoints
```

As noted in the lab overview, you have a lot of flexibility in defining the job's process topology and allocating hardware resources. Please refer to the [TFJob guide](https://www.kubeflow.org/docs/components/training/tftraining/) for more information.

The key field in the TFJob manifest is `tfReplicaSpecs`, which defines the number and the types of replicas (pods) created by a job. In our case, the job will start 3 workers using the container image defined in the `image` field and command line arguments defined in the `args` field.

Before submitting a job, you need to update the `image` and `args` fields with the values reflecting your environment.

Use your preferred command line editor or **Cloud Shell Editor** to update the `image` field with a full name of the image you created and pushed to your **Container Registry** in the previous step. You can retrieve the image name using the following command.

```bash
gcloud container images list
```

should have the following format:  `gcr.io/<YOUR_PROJECT_ID>/mnist-train`

Update manifest with project id, like below

```yaml
apiVersion: kubeflow.org/v1
kind: TFJob
metadata:
  name: multi-worker
spec:
  cleanPodPolicy: None
  tfReplicaSpecs:
    Worker:
      replicas: 3
      template:
        spec:
          containers:
          - name: tensorflow
            image: gcr.io/qwiklabs-gcp-01-93af833e6576/mnist-train
            args:
            - --epochs=5
            - --steps_per_epoch=100
            - --per_worker_batch=64
            - --saved_model_path=gs://qwiklabs-gcp-01-93af833e6576-bucket/saved_model_dir
            - --checkpoint_path=gs://qwiklabs-gcp-01-93af833e6576-bucket/checkpoints
```

Run it: `kubectl apply -f tfjob.yaml`

Recall that the job name was specified in the job manifest.

To retrieve logs generated by the training code you can use the `kubectl logs` command. Start by listing all pods created by the job.

Check pods status: 

`kubectl get pods`

```bash
JOB_NAME=multi-worker
kubectl describe tfjob $JOB_NAME
```

Check logs of executions: `kubectl logs --follow ${JOB_NAME}-worker-0 #or without the --follow flag` 


Delete everything: `kubectl delete tfjob $JOB_NAME`


## Creating a cloud storage bucket

As described in the lab overview, the distributed training script stores training checkpoints and the trained model in the _SavedModel_ format to the storage location passed as one of the script's arguments. You will use a **Cloud Storage** bucket as a shared persistent storage.

Since storage buckets are a global resource in Google Cloud you have to use a unique bucket name. For the purpose of this lab, you can use your project id as a name prefix.

```bash
export TFJOB_BUCKET=${PROJECT_ID}-bucket
gsutil mb gs://${TFJOB_BUCKET}
```


## Resources
- https://www.kubeflow.org/docs/components/training/tftraining/