# A HTTP python component using componentize-py

## Installing the requirements

Install Spin
https://developer.fermyon.com/spin/v3/install


To build the component, [`componentize-py`](https://pypi.org/project/componentize-py/) and [`spin-sdk`](https://pypi.org/project/spin-sdk/) are required. To install them, run:

```bash
uv sync
```

## Building and Running

```
spin up --build
```

## Spin kube

### Setup k8s env

Temp fix until nodes have the correct annotation applied automatically.
This annotation needs re-applying as nodes are cycled.
```
kubectl annotate node -l agentpool=usere4asv5  kwasm.sh/kwasm-node=true
```

Register executors in namespace
```
kubectl apply -f https://github.com/spinkube/spin-operator/releases/download/v0.4.0/spin-operator.shim-executor.yaml
```

### Build and deploy

Login to container registry using Azure CLI
```
az acr login -n tfsphoton
```

Push image to repository
```
spin registry push --build tfsphoton.azurecr.io/portals-transfers-webhook:latest
```

Deploy using generated manifest (originally generated using the `spin kube scaffold` command)
```
cd deployment/overlay/$ENV
kustomize build | kubectl -n portal-dev apply -f -
```
