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
SPIN_VARIABLE_DB_NAME=postgres SPIN_VARIABLE_DB_HOST=localhost SPIN_VARIABLE_DB_PASSWORD=password spin up --build
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
spin registry push --build ttl.sh/webhook-spin-app:24h

Deploy using generated manifest (originally generated using the `spin kube scaffold` command)
```
cd deployment/
kubectl -n spin apply -f manifest.yaml
```

Port forward to the service
```
kubectl -n spin port-forward svc/webhook-spin-app 3000:80
```

Curl to test
```
curl http://localhost:8080 -d '{"transfer_id": "d55a1306-95c7-44bc-a66d-60dfc4800752", "transfer_date":"2025-03-07", "value": 253644, "origin": "Third Financial", "status": "CREATED"}'
```

## Locust Performance/Load Test
```
uv run locust
```