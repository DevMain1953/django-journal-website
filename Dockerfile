# Download image of Ubuntu 20.04
FROM ubuntu:20.04

# To prevent interactive dialogs
ENV TZ=Europe \
    DEBIAN_FRONTEND=noninteractive

# Update and install necessary packages
# https://tecadmin.net/how-to-install-python-3-11-on-ubuntu-22-04/
RUN apt-get update \
# Install necessary packages to allow compilation of source code
    && apt-get install -y --no-install-recommends \
    tzdata \
    build-essential \
    checkinstall \
    libreadline-gplv2-dev \
    libncursesw5-dev \
    libssl-dev \
    libsqlite3-dev \
    tk-dev \
    libgdbm-dev \
    libc6-dev \
    libbz2-dev \
    software-properties-common \
# Install python 3.11
    && apt-get update \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get install -y --no-install-recommends \
    python3.11

# Install pip for Python 3.11
RUN apt-get install -y curl
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# Install poetry
ENV POETRY_VERSION 1.4.2
RUN python3.11 -m pip install "poetry==$POETRY_VERSION"

# Install dependencies
COPY . .
RUN poetry install

# Run poetry env
ENTRYPOINT ["poetry", "shell"]

# Go to website folder
WORKDIR /website

# Run Django server
CMD ["python3.11", "manage.py", "runserver"]