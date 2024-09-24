FROM python:3-slim

# Install dependencies for NSJail and Python packages
RUN apt-get -y update && apt-get install -y \
    autoconf \
    bison \
    flex \
    gcc \
    g++ \
    git \
    libprotobuf-dev \
    libnl-route-3-dev \
    libtool \
    make \
    pkg-config \
    protobuf-compiler \
    && rm -rf /var/lib/apt/lists/*

# Clone and build NSJail
RUN git clone https://github.com/google/nsjail.git /nsjail && \
    cd /nsjail && \
    make && \
    mv /nsjail/nsjail /usr/local/bin/nsjail && rm -rf -- /nsjail

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Install pip requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Expose port 8080
EXPOSE 8080

# Command to run the Flask app
CMD ["python3", "app.py"]