# End-to-End CI/CD Pipeline Automation with MLflow

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge\&logo=python)
![DVC](https://img.shields.io/badge/DVC-Data%20Version%20Control-orange?style=for-the-badge)
![MLflow](https://img.shields.io/badge/MLflow-Experiment%20Tracking-blue?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge\&logo=docker\&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-K3s-326CE5?style=for-the-badge\&logo=kubernetes\&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI/CD-2088FF?style=for-the-badge\&logo=githubactions\&logoColor=white)

---

# Project Overview

This project demonstrates a complete end-to-end MLOps workflow by implementing a fully automated CI/CD pipeline for machine learning using the Auto-MPG dataset. The system integrates modern machine learning infrastructure tools such as DVC, MLflow, GitHub Actions, Docker, and Kubernetes to ensure reproducibility, experiment tracking, automation, and scalable deployment.

The pipeline trains a Linear Regression model to predict vehicle fuel efficiency (MPG) while automating every stage of the machine learning lifecycle — from dataset versioning and experiment tracking to containerization and Kubernetes deployment.

The implementation highlights practical MLOps engineering concepts including:

* Data Version Control (DVC)
* Automated CI pipelines
* Experiment tracking with MLflow
* Docker-based containerization
* Kubernetes orchestration and scaling

---

# Architecture Diagram

```text
                 ┌──────────────────────┐
                 │   Auto-MPG Dataset   │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   DVC Data Tracking  │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    AWS S3 Remote     │
                 │   Artifact Storage   │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   train.py Script    │
                 │ Linear Regression ML │
                 └──────────┬───────────┘
                            │
          ┌─────────────────┴─────────────────┐
          ▼                                   ▼
┌──────────────────┐              ┌──────────────────┐
│  MLflow Logging  │              │   model.pkl      │
│  Metrics + Runs  │              │ Serialized Model │
└─────────┬────────┘              └─────────┬────────┘
          │                                  │
          └──────────────┬───────────────────┘
                         ▼
               ┌──────────────────┐
               │   DVC Pipeline   │
               │     (dvc.yaml)   │
               └────────┬─────────┘
                        │
                        ▼
              ┌────────────────────┐
              │ GitHub Actions CI  │
              │  Automated Re-run  │
              └────────┬───────────┘
                       │
                       ▼
              ┌────────────────────┐
              │   Docker Image     │
              │ sbkxd/auto-mpg...  │
              └────────┬───────────┘
                       │
                       ▼
              ┌────────────────────┐
              │ Kubernetes / K3s   │
              │   3 Replica Pods   │
              └────────────────────┘
```

---

# Tech Stack

| Technology       | Purpose                                |
| ---------------- | -------------------------------------- |
| Python 3.10      | Core programming language              |
| Git & GitHub     | Version control and repository hosting |
| DVC              | Dataset and pipeline versioning        |
| AWS S3           | Remote artifact storage for DVC        |
| MLflow           | Experiment tracking and metric logging |
| scikit-learn     | Linear Regression model training       |
| joblib           | Model serialization (.pkl storage)     |
| GitHub Actions   | Continuous Integration automation      |
| Docker           | Application containerization           |
| Kubernetes / K3s | Container orchestration and scaling    |

---

# Project Structure

```text
MLSD-CI-CD-MLflow/
│
├── Dataset/
│   ├── auto-mpg.data
│   ├── auto-mpg.names
│   ├── auto-mpg.data.dvc
│   └── auto-mpg.names.dvc
│
├── src/
│   └── train.py
│
├── model/
│   └── model.pkl
│
├── Notebooks/
│   └── experimentation.ipynb
│
├── mlruns/
│   └── MLflow tracking artifacts
│
├── .github/
│   └── workflows/
│       └── ml.yml
│
├── Dockerfile
├── deployment.yaml
├── dvc.yaml
├── dvc.lock
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Pipeline Walkthrough

## 1. Directory Setup and Git Initialization

The project workspace and repository structure were created to organize datasets, source code, models, notebooks, and MLflow artifacts.

### Commands

```bash
mkdir -p Dataset src model Notebooks mlruns
git init
```

---

## 2. DVC Initialization and Dataset Tracking

DVC was initialized to version-control machine learning datasets independently from Git.

### Commands

```bash
dvc init

dvc add Dataset/auto-mpg.data
dvc add Dataset/auto-mpg.names
```

This generated lightweight `.dvc` metadata files while keeping large datasets outside Git tracking.

---

## 3. AWS S3 Remote Storage Configuration

An AWS S3 bucket was configured as the remote storage backend for DVC artifacts and datasets.

### Commands

```bash
dvc remote add -d myremote s3://auto-mpg-project
dvc push
```

This synchronized local artifacts with cloud storage for reproducibility and distributed access.

---

## 4. ML Training Script Development

The training pipeline was implemented in `src/train.py` using Linear Regression with preprocessing, train-test split, MLflow logging, and model serialization.

### Features Implemented

* Data preprocessing
* 80-20 train-test split
* Linear Regression model training
* MLflow metric logging
* Model serialization using joblib

### Key Commands

```python
mlflow.start_run()
joblib.dump(model, "model/model.pkl")
```

---

## 5. DVC Pipeline Definition

A reproducible DVC pipeline stage was created linking:

* Input dataset
* Training script
* Output model artifact
* MLflow logs

### Command

```bash
dvc stage add -n train \
-d src/train.py \
-d Dataset/auto-mpg.data \
-o model/model.pkl \
-o mlruns \
python src/train.py
```

---

## 6. Pipeline Execution and Artifact Push

The DVC pipeline was executed and generated artifacts were pushed to remote storage.

### Commands

```bash
dvc repro
dvc push
```

This ensured reproducible training and remote artifact synchronization.

---

## 7. GitHub Actions CI Configuration

A CI workflow was configured using GitHub Actions to automate validation and pipeline execution on every repository push.

### Workflow Features

* Ubuntu VM provisioning
* Python dependency installation
* DVC dataset pulling
* Automated pipeline execution

### Trigger

```yaml
on: [push]
```

---

## 8. Dockerfile Authoring

A Docker container was created to package the ML application and dependencies.

### Dockerfile Base

```dockerfile
FROM python:3.10-slim
```

### Runtime Command

```dockerfile
CMD ["python", "-m", "http.server", "80"]
```

---

## 9. Docker Image Build and Push

The container image was built locally and pushed to DockerHub.

### Commands

```bash
docker build -t sbkxd/auto-mpg-project:v1.0 .
docker push sbkxd/auto-mpg-project:v1.0
```

DockerHub Image:

```text
sbkxd/auto-mpg-project:v1.0
```

---

## 10. Kubernetes Deployment Configuration

A Kubernetes deployment configuration was authored to orchestrate the containerized application.

### Features

* 3 replica pods
* NodePort service
* Port 80 exposure
* Fault tolerance and scalability

### Example

```yaml
replicas: 3
```

---

## 11. Deployment to K3s Cluster

The application was deployed to a local K3s Kubernetes cluster.

### Command

```bash
kubectl apply -f deployment.yaml
```

This launched three active pods with self-healing orchestration support.

---

## 12. MLflow Visualization

MLflow UI was used to visualize and monitor experiment metrics.

### Logged Metrics

* Mean Squared Error (MSE)
* R² Score

### Command

```bash
mlflow ui
```

---

# Model Performance

| Metric                   | Value |
| ------------------------ | ----- |
| Mean Squared Error (MSE) | 10.71 |
| R² Score                 | 0.79  |

---

# How to Reproduce

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/MLSD-CI-CD-MLflow.git
cd MLSD-CI-CD-MLflow
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

### Linux / Mac

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Pull Dataset from DVC Remote

```bash
dvc pull
```

---

## 5. Run the Pipeline

```bash
dvc repro
```

---

## 6. Launch MLflow UI

```bash
mlflow ui
```

Open in browser:

```text
http://127.0.0.1:5000
```

---

# CI/CD Workflow

The repository includes an automated GitHub Actions workflow defined in:

```text
.github/workflows/ml.yml
```

## Workflow Trigger

The workflow automatically executes whenever code is pushed to the repository.

```yaml
on: [push]
```

## Workflow Responsibilities

* Creates Ubuntu runner environment
* Installs Python dependencies
* Pulls datasets using DVC
* Reproduces ML pipeline
* Validates training execution
* Ensures reproducibility

This creates a fully automated CI validation pipeline for the machine learning workflow.

---

# Docker and Kubernetes Deployment

## Pull Docker Image

```bash
docker pull sbkxd/auto-mpg-project:v1.0
```

---

## Run Docker Container

```bash
docker run -p 80:80 sbkxd/auto-mpg-project:v1.0
```

---

## Deploy to Kubernetes

```bash
kubectl apply -f deployment.yaml
```

---

## Verify Pods

```bash
kubectl get pods
```

---

## Verify Services

```bash
kubectl get services
```

---

# MLflow Tracking

MLflow was integrated for experiment tracking and observability.

## Features Logged

* Model parameters
* Training metrics
* MSE
* R² Score
* Experiment runs
* Artifact storage

## Launch UI

```bash
mlflow ui
```

## Default Access URL

```text
http://127.0.0.1:5000
```

The dashboard enables visualization and comparison of training runs in real time.

---

# Limitations and Future Work

* Current implementation uses only a simple Linear Regression model.
* Hyperparameter tuning and advanced optimization techniques are not included.
* The deployment currently serves static artifacts rather than a production-grade inference API.
* Cloud-native Kubernetes deployment on AWS EKS/GKE is not yet implemented.
* Monitoring, alerting, and model drift detection can be integrated in future versions.
* CI/CD currently focuses mainly on Continuous Integration and can be extended toward full Continuous Deployment.

---

# Author

## S Bhanu Karthik

---

# References

* DVC Documentation: [https://dvc.org/doc](https://dvc.org/doc)
* MLflow Documentation: [https://mlflow.org/docs/latest/index.html](https://mlflow.org/docs/latest/index.html)
* Docker Documentation: [https://docs.docker.com/](https://docs.docker.com/)
* Kubernetes Documentation: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)

---

> This project demonstrates a practical implementation of modern MLOps principles including reproducibility, experiment tracking, CI/CD automation, containerization, and orchestration within a unified machine learning engineering workflow.
