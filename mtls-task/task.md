# Authentication Policies

create application as per below

```bash
kubectl create ns app1
kubectl label ns app1 istio-injection=enabled

kubectl create ns app2
kubectl label ns app2 istio-injection=enabled

kubectl create ns lapp


kubectl apply -n app1 -f  https://raw.githubusercontent.com/istio/istio/release-1.24/samples/httpbin/httpbin.yaml
kubectl apply -n app2 -f  https://raw.githubusercontent.com/istio/istio/release-1.24/samples/httpbin/httpbin.yaml
kubectl apply -n lapp -f  https://raw.githubusercontent.com/istio/istio/release-1.24/samples/httpbin/httpbin.yaml


kubectl apply -n app1 -f  https://raw.githubusercontent.com/istio/istio/release-1.24/samples/curl/curl.yaml
kubectl apply -n app2 -f  https://raw.githubusercontent.com/istio/istio/release-1.24/samples/curl/curl.yaml
kubectl apply -n lapp -f  https://raw.githubusercontent.com/istio/istio/release-1.24/samples/curl/curl.yaml

## To check Auto Mutual TLS

# check out the X-Forwarded-Client-Cert header
kubectl exec "$(kubectl get pod -l app=curl -n app1 -o jsonpath={.items[].metadata.name})" -c curl -n app1 -- curl http://httpbin:8000/headers

# Check out as no X-Forwarded-Client-Cert header wil be found
kubectl exec "$(kubectl get pod -l app=curl -n app1 -o jsonpath={.items[].metadata.name})" -c curl -n app1 -- curl http://httpbin.lapp:8000/headers
```


Globally Enabling the Istio mTLS

```yaml
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: "default"
  namespace: "istio-system"
spec:
  mtls:
    mode: STRICT

```

## Create policy for httpbin application in app2 to be STRICT mode but it should be disable for port 8080

https://istio.io/latest/docs/reference/config/security/peer_authentication/#:~:text=mode%3A%20STRICT-,Policy,-that%20enables%20strict

apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: app2
spec:
  selector:
    matchLabels:
      app: httpbin
  mtls:
    mode: STRICT
  portLevelMtls:  ### This is the container port and not the service port 
    8080: 
      mode: DISABLE
This allows traffic from lapp ns as container port is 8080 


## Create policy for httpbin application in app2 to be STRICT mode but it should be disable for port 8000

apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: app2
spec:
  selector:
    matchLabels:
      app: httpbin
  mtls:
    mode: STRICT
  portLevelMtls:  ### This is the container port and not the service port 
    8000: 
      mode: DISABLE
This does not allow traffic from lapp ns as service port is 8000

## check if global policy at root namespace is working
