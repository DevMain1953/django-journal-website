FROM ubuntu:20.04

# Update and install necessary packages
# https://tecadmin.net/how-to-install-python-3-11-on-ubuntu-22-04/
RUN sudo apt-get update \
# Install necessary packages to allow compilation of source code
    && apt-get install -y --no-install-recommends \
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
# Install python 3.11
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get install \
    python3.11

# Install pip for Python 3.11
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# Install poetry
ENV POETRY_VERSION 1.4.2
RUN pip3.11 install "poetry==$POETRY_VERSION"

# Install dependencies
RUN poetry install

# Run poetry env
ENTRYPOINT ["poetry", "shell"]

# Go to website folder
WORKDIR /website

# Run Django server
CMD ["python", "manage.py", "runserver"]