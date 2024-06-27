# Using alpine because of a smaller base image for building
FROM python:3.9-alpine AS builder

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

# Set work directory
WORKDIR $APP_HOME

# Install build dependencies
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    linux-headers

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Remove build dependencies
RUN apk del .build-deps

# Start a new stage for a smaller final image
FROM python:3.9-alpine

# Copy environment variables and workdir from builder
ENV SERVICE_NAME ${SERVICE_NAME}
ENV SERVICE_PORT ${SERVICE_PORT}
ENV SERVICE_METRICS_PORT ${SERVICE_METRICS_PORT}
ENV APP_HOME /opt/${SERVICE_NAME}
ENV PATH="${APP_HOME}/.local/bin:${PATH}"

# Set work directory
WORKDIR $APP_HOME

# Install make and any other runtime dependencies
RUN apk add --no-cache make

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy src directory (which includes service) and Makefile
COPY src ./src
COPY Makefile .

# Make ports available to the world outside this container
EXPOSE ${SERVICE_PORT} ${SERVICE_METRICS_PORT}

# Run the application via Makefile
CMD ["make", "run"]