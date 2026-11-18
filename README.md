\# GitOps Kubernetes Release Pipeline



End-to-end containerized release pipeline demonstrating automated CI validation, container vulnerability scanning, Helm packaging, and declarative GitOps reconciliation on Kubernetes.



\## Architecture



```text

GitHub Push / PR (main)

&#x20;  ├──► GitHub Actions (Layer 5 CI) ──► helm lint + helm template + docker build + Trivy CVE scan

&#x20;  └──► ArgoCD Controller (Layer 4 GitOps) ──► renders charts/release-app ──► Kubernetes (default namespace)

```



\## Tech Stack



\- \*\*Application:\*\* Python (Flask + Gunicorn) with `/healthz` readiness and liveness endpoint

\- \*\*Containerization \& Packaging (Layer 4):\*\* Docker, Helm (`charts/release-app`)

\- \*\*Orchestration \& GitOps (Layer 4):\*\* Kubernetes (`kind`), ArgoCD (automated sync, pruning, and self-healing)

\- \*\*CI \& Security Gating (Layer 5):\*\* GitHub Actions, Aqua Trivy (`CRITICAL` CVE gate)



\## Repository Structure



```text

k8s-release-pipeline/

├── .github/workflows/ci.yml   # CI pipeline: Helm lint/template, Docker build, Trivy scan

├── argocd/application.yaml    # Declarative ArgoCD Application manifest

├── charts/release-app/        # Parameterized Helm chart (Deployment, Service, values.yaml)

├── app.py                     # Flask application with /healthz probe endpoint

├── Dockerfile                 # Multi-worker Gunicorn container image definition

├── requirements.txt           # Python dependencies

├── .gitignore                 # Local environment exclusions

└── README.md                  # Architecture and setup guide

```



\## Prerequisites



\- Docker Desktop (running)

\- `kind`, `kubectl`, and `helm` installed locally



\## Quickstart



1\. \*\*Create a local `kind` cluster and load the application image:\*\*

&#x20;  ```bash

&#x20;  kind create cluster

&#x20;  docker build -t release-app:latest .

&#x20;  kind load docker-image release-app:latest

&#x20;  ```



2\. \*\*Install ArgoCD in the `argocd` namespace:\*\*

&#x20;  ```bash

&#x20;  kubectl create namespace argocd

&#x20;  kubectl apply --server-side --force-conflicts -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

&#x20;  ```



3\. \*\*Register the declarative ArgoCD Application:\*\*

&#x20;  ```bash

&#x20;  kubectl apply -f argocd/application.yaml

&#x20;  ```



4\. \*\*Access the ArgoCD UI (`\[https://127.0.0.1:8081](https://127.0.0.1:8081)`):\*\*

&#x20;  ```bash

&#x20;  # Retrieve initial admin password (PowerShell)

&#x20;  \[System.Text.Encoding]::UTF8.GetString(\[System.Convert]::FromBase64String((kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}")))



&#x20;  # Open local tunnel to ArgoCD API server

&#x20;  kubectl port-forward --address 127.0.0.1 svc/argocd-server -n argocd 8081:443

&#x20;  ```



\## Verifying GitOps Auto-Sync



1\. Update `replicaCount` in `charts/release-app/values.yaml` and push to `main`.

2\. GitHub Actions validates the Helm chart and scans the container image with Trivy.

3\. ArgoCD detects the new commit, reconciles cluster state automatically, and scales the `Deployment` pods with zero manual `kubectl` or `helm` commands.

