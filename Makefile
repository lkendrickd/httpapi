# Variables
PYTHON := python3
PIP := $(PYTHON) -m pip
DOCKER := docker
IMAGE_NAME ?= fastapi-app
VERSION ?= $(shell cat version 2>/dev/null || echo "0.0.1")

# Service Configuration Variables
SERVICE_NAME ?= fastapi-service
SERVICE_LOG_LEVEL ?= INFO
SERVICE_CONFIG_FILE ?= config.yaml
SERVICE_PORT ?= 9000
SERVICE_HOST ?= 0.0.0.0
SERVICE_METRICS_PORT ?= 8000
SERVICE_HOME ?= /opt/$(SERVICE_NAME)

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  help        : Show this help message"
	@echo "  dependency_install: Install dependencies"
	@echo "  dependency_freeze : Freeze dependencies"
	@echo "  run         : Run the service locally"
	@echo "  test        : Run tests"
	@echo "  lint        : Run linter"
	@echo "  clean       : Remove build artifacts and cache files"
	@echo "  docker-build: Build Docker image"
	@echo "  docker-run  : Run Docker container"
	@echo "  docker-stop : Stop Docker container"

.PHONY: dependency_install
dependency_install:
	$(PIP) install -r requirements.txt

.PHONY: dependency_freeze
dependency_freeze:
	$(PIP) freeze > requirements.txt

.PHONY: config
config:
	@echo "Creating config file: $(SERVICE_CONFIG_FILE)"
	@echo "# FastAPI Service Configuration" > $(SERVICE_CONFIG_FILE)
	@echo "app_name: \"$(SERVICE_NAME)\"" >> $(SERVICE_CONFIG_FILE)
	@echo "debug: false" >> $(SERVICE_CONFIG_FILE)
	@echo "host: \"$(SERVICE_HOST)\"" >> $(SERVICE_CONFIG_FILE)
	@echo "port: $(SERVICE_PORT)" >> $(SERVICE_CONFIG_FILE)
	@echo "metrics_port: $(SERVICE_METRICS_PORT)" >> $(SERVICE_CONFIG_FILE)
	@echo "log_level: \"$(SERVICE_LOG_LEVEL)\"" >> $(SERVICE_CONFIG_FILE)
	@echo "version: \"$$(cat version)\"" >> $(SERVICE_CONFIG_FILE)
	@echo "commit: \"$$(git rev-parse --short HEAD || echo 'unknown')\"" >> $(SERVICE_CONFIG_FILE)
	@echo "branch: \"$$(git rev-parse --abbrev-ref HEAD || echo 'unknown')\"" >> $(SERVICE_CONFIG_FILE)
	@echo "build_date: \"$$(date -u +'%Y-%m-%dT%H:%M:%SZ')\"" >> $(SERVICE_CONFIG_FILE)
	@echo "# Add any other configuration parameters here" >> $(SERVICE_CONFIG_FILE)
	@echo "Config file created successfully."

.PHONY: run
run:
	@if [ -f $(SERVICE_CONFIG_FILE) ]; then \
       echo "Using configuration file: $(SERVICE_CONFIG_FILE)"; \
       $(PYTHON) src/service/main.py --config $(SERVICE_CONFIG_FILE); \
    else \
       echo "No configuration file found. Using default settings."; \
       $(PYTHON) src/service/main.py --port $(SERVICE_PORT) --metrics-port $(SERVICE_METRICS_PORT); \
    fi

.PHONY: docker-build
docker-build:
	$(DOCKER) build -t $(IMAGE_NAME):$(VERSION) \
		--build-arg SERVICE_NAME=$(SERVICE_NAME) \
        --build-arg SERVICE_PORT=$(SERVICE_PORT) \
        --build-arg SERVICE_METRICS_PORT=$(SERVICE_METRICS_PORT) \
        -f build/Dockerfile .

.PHONY: docker-run
docker-run: docker-build
	$(DOCKER) run --rm -it \
		--name $(SERVICE_NAME) \
		-e SERVICE_NAME=$(SERVICE_NAME) \
		-e SERVICE_HOST=$(SERVICE_HOST) \
		-e SERVICE_PORT=$(SERVICE_PORT) \
		-e SERVICE_METRICS_PORT=$(SERVICE_METRICS_PORT) \
		-e SERVICE_LOG_LEVEL=$(SERVICE_LOG_LEVEL) \
		-e APP_HOME=$(SERVICE_HOME) \
		-p $(SERVICE_PORT):$(SERVICE_PORT) \
		-p $(SERVICE_METRICS_PORT):$(SERVICE_METRICS_PORT) \
		$(IMAGE_NAME):$(VERSION)
.PHONY: test
test:
	pytest tests

.PHONY: lint
lint:
	$(PIP) show flake8 || $(PIP) install flake8
	flake8 src/service
	@if [ $$? -eq 0 ]; then echo "Linting Passed"; exit 0; fi

.PHONY: clean
clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf src/**/__pycache__

.PHONY: version
version:
	@echo $(VERSION)