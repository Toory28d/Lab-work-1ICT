# Lab Work #3 — Report

## Objective
Containerize a Flask API using Docker, deploy three replicas using Kubernetes, observe request distribution, demonstrate self-healing, and scale replicas.

## Part A — Docker
- Docker image: `lab3-flask:local`
- Build command: `docker build -t lab3-flask:local .`
- Run command: `docker run --rm -p 5000:5000 lab3-flask:local`
- Compose command: `docker compose up --build -d`
- Actual result: **TO BE FILLED AFTER EXECUTION**
- Screenshots: `screenshots/docker-build.png`, `screenshots/docker-run.png`, `screenshots/compose.png`

## Part B — Kubernetes
- Deployment: `lab3-web`, desired replicas: 3
- Service: `lab3-web-service`, ClusterIP, port 80 -> 5000
- Actual ready replicas: **TO BE FILLED**
- Hostnames observed in 30 requests: **TO BE FILLED**
- Screenshot: `screenshots/k8s-pods.png`, `screenshots/distribution.png`

## Part C — Self-healing and scaling
- Deleted pod: **TO BE FILLED**
- Replacement pod: **TO BE FILLED**
- Time until ready: **TO BE FILLED**
- Scaling 3 -> 5 -> 2, actual ready counts: **TO BE FILLED**
- Screenshots: `screenshots/self-healing.png`, `screenshots/scaling.png`

## Reflection Questions

1. **What is Docker?** Docker packages the application and dependencies into an image; containers run isolated instances of that image.
2. **Why Kubernetes?** Kubernetes manages desired replicas, scheduling, Service discovery, health probes, and recovery from pod failures.
3. **Deployment vs Service?** Deployment maintains pods and desired replica counts. Service provides a stable network endpoint and distributes connections to ready pods.
4. **What happens if a pod fails?** The Deployment controller creates a replacement to restore the requested number of replicas; liveness probes can restart unhealthy containers.
5. **How does scaling work?** Updating `spec.replicas` changes the desired pod count; the Deployment controller adds or removes pods.
6. **What limits were observed?** **TO BE FILLED with evidence from local execution.**

## Conclusion
**TO BE FILLED after completing the experiments.** Compare the observations with the expected results and explain any discrepancies.

## Evidence status
Source code and configuration are provided. Real Kubernetes execution, screenshots, and measurements must be completed on the student's environment.
