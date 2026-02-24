## Network Security ML Project – Phishing Detection

This repository contains a **Network Security / Phishing Detection** machine learning project that builds an end‑to‑end pipeline for detecting malicious or phishing network traffic. It covers data ingestion, preprocessing, model training with multiple algorithms, experiment tracking, model persistence, containerization with Docker, and deployment on an AWS EC2 instance with a CI/CD pipeline powered by GitHub Actions.

The core goal is to provide a production‑oriented workflow for **Network Security Projects for Phishing Data**: starting from raw data and ending with a deployed model that can be continuously improved and redeployed automatically.

---

## High‑Level Architecture

- **Data ingestion & preprocessing**
  - Loads phishing / network security data from local or remote sources.
  - Cleans data, handles missing values, encodes categorical features, and scales numerical features.
  - Produces transformed NumPy arrays and serialized preprocessing objects for reuse in training and inference.

- **Model training & selection**
  - Trains multiple classifiers (e.g. Random Forest, Gradient Boosting, Decision Tree, Logistic Regression, KNN).
  - Performs hyperparameter tuning using grid search–style parameter grids.
  - Evaluates models on training and test sets using classification metrics (F1, precision, recall, etc.).
  - Selects the best model based on evaluation scores and logs results to **MLflow** (tracked via **DagsHub**).

- **Experiment tracking**
  - Uses `mlflow` integrated with DagsHub (`dagshub.init`) to track runs, metrics, and models.
  - Each training run logs:
    - F1 score
    - Recall
    - Precision
    - Trained model artifact

- **Model packaging**
  - Wraps the best model together with the preprocessing pipeline in a custom `NetworkModel` wrapper.
  - Persists both the full pipeline and the raw best model to disk (e.g. `final_model/model.pkl`) for later inference or deployment.

- **Deployment & operations**
  - Dockerized application suitable for deployment on an **AWS EC2** instance.
  - CI/CD implemented using **GitHub Actions**, building and pushing Docker images to **AWS ECR**, and deploying updates to EC2.

---

## Project Structure

> Note: Exact files may evolve over time; this is the conceptual structure and responsibilities.

- `network_security/`
  - `components/`
    - `model_trainer.py`: Orchestrates model training; loads transformed train/test arrays, trains multiple models, chooses the best one, logs metrics to MLflow/DagsHub, and saves the final model artifacts.
    - (Other components likely exist for data ingestion, validation, and transformation.)
  - `entity/`
    - `artifact_entity.py`: Defines artifact dataclasses such as `DataTransformationArtifact`, `ClassificationMetricArtifact`, and `ModelTrainerArtifact` to pass structured outputs between pipeline steps.
    - `config_entity.py`: Defines configuration dataclasses such as `ModelTrainerConfig` for paths and hyperparameters.
  - `utils/`
    - `utils.py`: Utility helpers like `save_object`, `load_object`, `load_numpy_array_data`.
    - `ml_utils.py`: Model utilities such as `evaluate_models` and `get_classification_score`.
    - `model/estimator.py`: Defines the `NetworkModel` wrapper that bundles the preprocessor and underlying ML model.
  - `logging/`
    - `logger.py`: Centralized logging configuration and logger instance.
  - `exception/`
    - `exception.py`: Custom exception types (e.g. `CustomException`) for consistent error handling across the project.
  - (Optional) `pipeline/`: High‑level pipeline scripts (e.g. training/inference pipelines).
  - (Optional) `config/` or `constants/`: Global configuration values and constants.

- `notebooks/` (if present)
  - Exploratory data analysis (EDA), feature exploration, and initial experimentation with models and preprocessing.

- `final_model/`
  - Contains the final trained model serialized object(s), such as `model.pkl`.

- `.github/workflows/`
  - YAML workflow files defining GitHub Actions CI/CD pipelines for building, testing, pushing Docker images, and deploying to EC2.

- `Dockerfile`, `docker-compose.yml` (if present)
  - Define how the application is containerized and run locally or in production.

- `README.md`
  - This documentation file.

---

## Key ML Training Logic (Example: `model_trainer.py`)

The `ModelTrainer` class (located under `network_security/components/model_trainer.py`) is responsible for:

- Loading transformed training and test NumPy arrays.
- Splitting features and labels.
- Training multiple candidate models with predefined hyperparameter grids.
- Evaluating each model using classification metrics.
- Selecting the best model based on evaluation results.
- Logging metrics and the model to MLflow/DagsHub.
- Saving the combined `NetworkModel` (preprocessor + model) and the raw best model to disk.

This encapsulation makes it easier to:

- Re‑run experiments with different configurations.
- Track all runs through MLflow.
- Swap models or modify hyperparameters without changing the rest of the pipeline.

---

## Getting Started

### 1. Local Setup

- **Prerequisites**
  - Python 3.8+ (recommended)
  - pip / conda
  - Git
  - (Optional) Virtual environment tools like `venv` or `conda`

- **Clone the repository**

```bash
git clone <YOUR_REPO_URL>
cd "Cyber-security ML Project"
```

- **Create and activate virtual environment (optional but recommended)**

```bash
python -m venv venv
source venv/bin/activate         # Linux / macOS
# or
venv\Scripts\activate            # Windows
```

- **Install dependencies**

```bash
pip install -r requirements.txt
```

### 2. Running Training

Depending on how your pipeline is wired, you will typically:

- Configure input data paths and other settings in a config file or environment variables.
- Run a training script or pipeline entrypoint, such as:

```bash
python main.py          # or
python -m network_security.pipeline.training_pipeline
```

(Adjust the command to match your actual entry script.)

This will:

- Load and preprocess the phishing/network security dataset.
- Train multiple candidate models and select the best one.
- Log metrics to MLflow/DagsHub.
- Save the final model artifacts to the `artifacts/` or `final_model/` directory.

---

## GitHub Secrets for CI/CD

To enable the CI/CD pipeline and deployment to AWS with Docker and ECR, configure the following secrets in your GitHub repository settings under **Settings → Secrets and variables → Actions**:

- **AWS_ACCESS_KEY_ID**
- **AWS_SECRET_ACCESS_KEY**
- **AWS_REGION**
- **AWS_ECR_LOGIN_URI**
- **ECR_REPOSITORY_NAME**

These secrets are used by GitHub Actions to:

- Authenticate with AWS.
- Log in to Amazon ECR.
- Build and push Docker images.
- Deploy the updated container to your EC2 instance.

---

## Docker & Deployment on AWS EC2

This project is designed to be containerized with Docker and deployed to an **AWS EC2** instance.

### 1. Docker Setup on EC2

SSH into your EC2 instance (Ubuntu is assumed) and run:

```bash
# optional but recommended
sudo apt-get update -y
sudo apt-get upgrade

# required: install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# add the ubuntu user to the docker group
sudo usermod -aG docker ubuntu
newgrp docker
```

This will:

- Install Docker.
- Allow the `ubuntu` user to run Docker commands without `sudo`.

### 2. Pull and Run the Docker Image

Once your CI/CD pipeline has pushed an image to ECR:

```bash
aws ecr get-login-password --region $AWS_REGION \
  | docker login --username AWS --password-stdin $AWS_ECR_LOGIN_URI

docker pull $AWS_ECR_LOGIN_URI/$ECR_REPOSITORY_NAME:latest

docker run -d --name network-security-ml -p 80:80 \
  $AWS_ECR_LOGIN_URI/$ECR_REPOSITORY_NAME:latest
```

(Adjust ports and container names as needed.)

---

## CI/CD with GitHub Actions

This project is configured to use **GitHub Actions** for continuous integration and continuous deployment:

- **On push / PR to main (or a specific branch):**
  - Run tests and basic checks.
  - Build a Docker image for the application.
  - Authenticate to AWS using the configured GitHub secrets.
  - Push the Docker image to **AWS ECR**.
  - SSH into the target **EC2 instance** (or use AWS SSM, depending on your workflow) and:
    - Pull the latest image from ECR.
    - Restart the container with the new image.

This ensures that:

- Every change pushed to the repo can be automatically validated.
- Successfully built images are deployed to your EC2 instance without manual intervention.

---

## Experiment Tracking with MLflow & DagsHub

The training code integrates with **DagsHub** for experiment tracking:

- Uses `dagshub.init(repo_owner='avitanov', repo_name='Network-Security-ML', mlflow=True)` to connect.
- Every training run:
  - Starts an MLflow run.
  - Logs metrics: F1 score, recall, precision.
  - Logs the trained model with `mlflow.sklearn.log_model`.

You can browse runs, compare models, and download artifacts directly from the DagsHub UI for this repository.

---

## Summary

- This repository implements an end‑to‑end **Network Security / Phishing Detection** ML pipeline.
- It includes modular components for preprocessing, training, evaluation, logging, and packaging models.
- The project is **dockerized**, **deployed on AWS EC2**, and uses **GitHub Actions** for CI/CD with images stored in **AWS ECR**.
- ML experiments are tracked with **MLflow** integrated through **DagsHub**.

Cyber-security End-End ML Project