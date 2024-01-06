FROM python:3.11-bullseye

# Set the working directory to /app
WORKDIR /app

# Dev experience
COPY Makefile ./
COPY pyproject.toml ./
RUN --mount=type=cache,target=/root/.cache/pip make install-dev 
RUN pyright .

COPY . /app
RUN pip install -e .