FROM ubuntu:20.04

# Install python as global module
RUN sudo apt update \
    && sudo apt install software-properties-common \
    && sudo apt update \
    && sudo apt install python3.11

# Install poetry
ENV POETRY_VERSION 1.4.2
RUN pip install "poetry==$POETRY_VERSION"

# Install packages
RUN poetry install