# syntax=docker/dockerfile:1

# Global ARG declarations (available to the entire Dockerfile)
ARG PROJ_SHORT_NAME=twp


# Stage 1: Base image.
FROM amazonlinux:2023.6.20241031.0 AS base

# Local ARG declarations
ARG PROJ_SHORT_NAME

# Install the essential system packages.
RUN dnf install -y wget tar gzip python3-pip shadow-utils openssl

# Create a non-privileged user
RUN useradd -r -s /usr/sbin/nologin ${PROJ_SHORT_NAME}

# Install Supervisor.
RUN python3 -m pip install supervisor

# Create necessary directories and set permissions
RUN set -x \
  && mkdir -p /opt/twp/auth/{src,data,log,conf,system} \
  && chown -R ${PROJ}:${PROJ} /opt/twp


# Stage 2: Build stage.
FROM base AS build

# Set the application directory
WORKDIR /opt/twp/auth

# Create a virtual environment
RUN python3 -m venv venv

# Activate the virtual environment and install dependencies in the same shell
COPY --from=src requirements.txt .
RUN bash -c "source venv/bin/activate && pip install -r requirements.txt"


# Stage 3: Development image
FROM base AS dev

# Install the system packages required for debugging.
RUN dnf install -y less procps net-tools iputils bind-utils vim-minimal

# Copy the installed packages from the builder stage
COPY --from=build /opt/twp/auth/venv /opt/twp/auth/venv

# Set default work directory.
WORKDIR /opt/twp/auth
