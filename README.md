# Lab Work #3 — Docker and Kubernetes

A small Flask REST API packaged with Docker and deployed as three replicas in Kubernetes. The API returns the hostname of the pod serving each request.

## Requirements

- Python 3.12+ (optional for local tests)
- Docker Desktop (Linux containers)
- Kubernetes enabled in Docker Desktop, or minikube with the image loaded
- `kubectl`

## Part A: Docker

```powershell
docker build -t lab3-flask:local .
docker run --rm -p 5000:5000 lab3-flask:local
```

In another terminal:

```powershell
Invoke-RestMethod http://localhost:5000/
Invoke-RestMethod http://localhost:5000/health
```

For Docker Compose (stop the `docker run` container first):

```powershell
docker compose up --build -d
docker compose ps
Invoke-RestMethod http://localhost:5000/info
docker compose down
```

## Part B: Kubernetes (Docker Desktop)

Enable Kubernetes in Docker Desktop settings and wait for it to be ready. Ensure Docker Desktop uses the same local image store as your cluster. If using minikube, run `minikube image load lab3-flask:local` after building.

```powershell
kubectl config current-context
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl rollout status deployment/lab3-web --timeout=120s
kubectl get deployments,pods,services -l app=lab3-web
kubectl get pods -l app=lab3-web -o wide
kubectl port-forward service/lab3-web-service 8080:80
```

Keep port-forward running. In another PowerShell terminal:

```powershell
1..20 | ForEach-Object { (Invoke-RestMethod http://localhost:8080/).hostname }
.\scripts\check_distribution.ps1 -Count 30
```

The hostnames should include multiple pods (not necessarily every pod in a small sample). Kubernetes Service balances connections; reuse of connections can affect the observed distribution.

## Part C: Self-healing and scaling

Take a screenshot of the pod list before deletion. Then:

```powershell
kubectl get pods -l app=lab3-web
$pod = kubectl get pods -l app=lab3-web -o jsonpath='{.items[0].metadata.name}'
kubectl delete pod $pod
kubectl get pods -l app=lab3-web -w
```

Stop the watch with Ctrl+C. The Deployment should create a replacement pod. Then scale:

```powershell
kubectl scale deployment/lab3-web --replicas=5
kubectl rollout status deployment/lab3-web
kubectl get pods -l app=lab3-web
kubectl scale deployment/lab3-web --replicas=2
kubectl get pods -l app=lab3-web
```

### Cleanup

```powershell
kubectl delete -f k8s/service.yaml
kubectl delete -f k8s/deployment.yaml
```

## Tests

```powershell
python -m pip install -r requirements.txt
python -m pytest tests/ -v
```

## Evidence and submission

Save actual screenshots in `screenshots/`: `docker-build.png`, `docker-run.png`, `compose.png`, `k8s-pods.png`, `distribution.png`, `self-healing.png`, `scaling.png`. Fill in `REPORT.md` with observed values and explanations. Do not claim tests or Kubernetes operations succeeded unless you actually ran them.

## Git

Place this directory in the existing `Lab-work-1ICT` repository as `Lab3/`, commit and push:

```powershell
git add Lab3
git commit -m "Add Lab 3 Docker and Kubernetes deployment"
git push origin main
```
