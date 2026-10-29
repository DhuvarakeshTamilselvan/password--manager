# Password Manager (Basic) — DevOps Course Project

This starter project follows the required workflow: VS Code → GitHub → Jenkins → Docker → Docker Hub → Kubernetes.

## Features by version
- **v1**: Add credentials and show the number of entries.
- **v2**: Add and view credential entries.
- **v3**: Add, view, and delete credential entries.
- `/health` endpoint for health checks.

> **Security warning:** This is a classroom demonstration only. Credentials are stored in process memory as plaintext and disappear when the app restarts. Use only fake/dummy credentials. Do not use this app to store real passwords. A real password manager needs authentication, encryption, secure persistence, CSRF protection, and additional security review.

## 1. Run locally (Windows PowerShell)
Open a terminal in this folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:APP_VERSION = "v1"
python app.py
```

Open http://localhost:5000. Stop with `Ctrl+C`. For v2/v3, change `APP_VERSION` to `v2` or `v3` and restart.

If PowerShell blocks activation, use:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

## 2. Git and GitHub
Create an empty repository on GitHub, then run (replace the URL):

```powershell
git init
git add .
git commit -m "Add Password Manager v1-v3 starter"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

This starter keeps all three implementations in one repository so the Jenkins pipeline can build any version. If your instructor specifically requires separate branches, create them after committing the starter:
```powershell
git switch -c v1
git push -u origin v1
git switch main
git switch -c v2
git push -u origin v2
git switch main
git switch -c v3
git push -u origin v3
```
These branches initially contain the same files. If you use branches for assessment, make a meaningful commit in each branch and document the changes.

## 3. Docker
Make sure Docker Desktop is running:
```powershell
docker build --build-arg VERSION=v1 -t YOUR_DOCKERHUB_USERNAME/password-manager:v1 .
docker run --rm -p 5001:5000 -e APP_VERSION=v1 YOUR_DOCKERHUB_USERNAME/password-manager:v1
```
Open http://localhost:5001. Stop with `Ctrl+C`.

Build and push each version (replace your username):
```powershell
docker login
docker build --build-arg VERSION=v1 -t YOUR_DOCKERHUB_USERNAME/password-manager:v1 .
docker push YOUR_DOCKERHUB_USERNAME/password-manager:v1
docker build --build-arg VERSION=v2 -t YOUR_DOCKERHUB_USERNAME/password-manager:v2 .
docker push YOUR_DOCKERHUB_USERNAME/password-manager:v2
docker build --build-arg VERSION=v3 -t YOUR_DOCKERHUB_USERNAME/password-manager:v3 .
docker push YOUR_DOCKERHUB_USERNAME/password-manager:v3
```

## 4. Jenkins
1. Install Jenkins and the Git/Pipeline plugins.
2. Add a Jenkins credential with ID `dockerhub-creds` (Username with password; use a Docker Hub access token as the password).
3. Create a Pipeline job configured to use this repository and its `Jenkinsfile`.
4. Ensure the Jenkins agent has Python, Docker CLI/daemon access, and `kubectl` configured if using the deploy stage.
5. Run with parameter `VERSION` set to `v1`, `v2`, or `v3`.

The supplied Jenkinsfile builds and pushes the selected image. Kubernetes deployment is a separate stage and requires a configured cluster context and image names that match your Docker Hub repository.

## 5. Kubernetes
Edit `k8s/v1.yaml`, `k8s/v2.yaml`, and `k8s/v3.yaml`: replace `YOUR_DOCKERHUB_USERNAME` in each image field.

Apply the manifests:
```powershell
kubectl apply -f k8s/v1.yaml
kubectl apply -f k8s/v2.yaml
kubectl apply -f k8s/v3.yaml
kubectl get deployments
kubectl get pods
kubectl get services
```

For Minikube, access each service:
```powershell
minikube service password-v1-service
minikube service password-v2-service
minikube service password-v3-service
```

NodePorts are 30001, 30002, and 30003. Whether direct `localhost:30001` works depends on your Kubernetes setup; `minikube service` is the reliable local access command.

## 6. Suggested evidence screenshots
- V1, V2, and V3 in a browser
- GitHub repository and commits/branches
- Jenkins successful build
- Docker Hub with v1/v2/v3 tags
- `kubectl get deployments`, `kubectl get pods`, and `kubectl get services`

## Troubleshooting
- `python` not recognized: install Python and enable “Add Python to PATH”, then reopen VS Code.
- `git` not recognized: install Git for Windows, then reopen VS Code.
- `docker` not recognized or daemon error: start Docker Desktop and wait until it is running.
- Pod image pull error: confirm the image tag exists and the Docker Hub username is correct.
- Jenkins Docker permission error: the Jenkins agent needs access to the Docker daemon; configure this on the machine rather than hard-coding credentials.
