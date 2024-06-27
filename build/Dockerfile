# Use an official Python Alpine runtime as a parent image
FROM python:3.9-alpine

# Define build arguments
ARG SERVICE_NAME=fastapi-service
ARG SERVICE_PORT=9000
ARG SERVICE_METRICS_PORT=8000

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SERVICE_NAME ${SERVICE_NAME}
ENV SERVICE_PORT ${SERVICE_PORT}
ENV SERVICE_METRICS_PORT ${SERVICE_METRICS_PORT}
ENV APP_HOME /opt/${SERVICE_NAME}
ENV PATH="${APP_HOME}/.local/bin:${PATH}"

# Set work directory
WORKDIR $APP_HOME

# Install system dependencies
RUN apk update && apk add --no-cache \
    build-base \
    linux-headers

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy service directory
COPY service ./service

# Copy Makefile
COPY Makefile .

# Make ports available to the world outside this container
EXPOSE ${SERVICE_PORT} ${SERVICE_METRICS_PORT}

# Run the application via Makefile
CMD ["make", "run"]