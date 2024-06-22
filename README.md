# httpapi

A production-ready microservice using FastAPI.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
pip install -r requirements.txt
```

## Usage

```bash
uvicorn service.main:app --host 0.0.0.0 --port 8000
```

## Endpoints

- `/health`: Health check endpoint
- `/metrics`: Prometheus metrics endpoint
- `/`: Root endpoint
