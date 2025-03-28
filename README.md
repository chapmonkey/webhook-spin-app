# A Webhook handling Spin application
A simple Spin application using the python component using `componentize-py` and `spin-sdk`

## Installing the requirements

Install UV
https://docs.astral.sh/uv/

Install Spin
https://developer.fermyon.com/spin/v3/install

Spin Kube Plugin
https://github.com/spinframework/spin-plugin-kube

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

Install Spin kube
https://www.spinkube.dev/docs/install/

### Build and deploy

Push image to repository
```
spin registry push --build ttl.sh/webhook-spin-app:24h
```

Deploy using generated manifest (originally generated using the `spin kube scaffold` command)
```
cd deployment/
kubectl -n spin apply -f manifest.yaml
```

## Testing

If the application is running in Kubernetes then port forward to the service
```
kubectl -n spin port-forward svc/webhook-spin-app 3000:80
```

Curl to test
```
curl http://localhost:3000 -d '{"transfer_id": "d55a1306-95c7-44bc-a66d-60dfc4800752", "transfer_date":"2025-03-07", "value": 253644, "origin": "Third Financial", "status": "CREATED"}'
```

Locust Performance/Load Test
```
uv run locust
```