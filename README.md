# End-to-End MLOps Pipeline: Auto-MPG Prediction

**Author:** S Bhanu Karthik
## Project Overview

This repository demonstrates a complete, production-grade Machine Learning Operations (MLOps) architecture. The underlying machine learning task utilizes a Linear Regression model to predict the fuel efficiency (MPG) of various vehicles based on the classic Auto-MPG dataset.

The primary objective of this project is the implementation of a robust infrastructure lifecycle, encompassing data versioning, continuous integration, containerization, deployment orchestration, and experiment observability.

## Technology Stack

* **Machine Learning:** Python, scikit-learn, pandas
* **Experiment Tracking & Observability:** MLflow
* **Data Version Control:** DVC, AWS S3
* **Continuous Integration:** GitHub Actions
* **Containerization:** Docker
* **Deployment & Orchestration:** Kubernetes (K3s)

## Repository Structure

```text
.
├── .github/workflows/
│   └── ml.yml                 # GitHub Actions CI pipeline configuration
├── Dataset/
│   ├── auto-mpg.data          # Raw dataset (Tracked via DVC, ignored by Git)
│   ├── auto-mpg.names         # Dataset metadata
│   └── auto-mpg.data.dvc      # DVC metadata pointer for S3 remote
├── model/
│   └── model.pkl              # Serialized ML model (Generated post-training)
├── src/
│   └── train.py               # ML training script with MLflow integration
├── mlruns/                    # Local MLflow artifact storage
├── .dvc/                      # DVC configuration directory
├── Dockerfile                 # Containerization instructions
├── deployment.yaml            # Kubernetes declarative deployment configuration
└── requirements.txt           # Python dependencies

```

## Architecture and Workflow

### 1. Data Versioning (DVC & AWS S3)

The raw datasets are tracked using Data Version Control (DVC) to prevent large file inflation within the Git repository. The `.dvc` tracking files are committed to Git, while the actual data binaries are pushed to an AWS S3 bucket. This ensures the training data is highly available and strictly version-controlled alongside the source code.

### 2. Model Training and Observability (MLflow)

The training logic is encapsulated in `src/train.py`. The script performs data preprocessing, an 80-20 train-test split, and model fitting. MLflow is integrated directly into the script to automatically log hyperparameters, Mean Squared Error (MSE), R-squared metrics, and the serialized model artifacts.

### 3. Continuous Integration (GitHub Actions)

A CI pipeline is configured to trigger automatically upon every push to the repository. The cloud runner provisions an Ubuntu environment, authenticates with AWS, pulls the latest dataset via DVC, and executes the training pipeline (`dvc repro`). The resulting MLflow metrics are packaged and uploaded as a build artifact for post-execution review.

### 4. Containerization (Docker)

The application, its runtime environment, and the serialized model (`model.pkl`) are packaged into an isolated Docker container. This guarantees execution consistency across local, testing, and production environments.

### 5. Orchestration (Kubernetes)

The containerized application is deployed utilizing a declarative Kubernetes configuration (`deployment.yaml`). The deployment manages three distinct application replicas to ensure high availability, fault tolerance, and load distribution, exposed locally via a NodePort service.

## Local Execution Instructions

### Prerequisites

* Python 3.10+
* Docker Desktop
* Kubernetes (K3s or Minikube)
* AWS CLI configured with active credentials
kubectl expose deployment ml-project-deployment --type=NodePort --port=80

```
