FROM python:3.11-slim
WORKDIR /app

RUN apt update && apt install -y \
    build-essential \
    gcc \
    g++ \
    cmake \
    make \
    python3-dev \
    libpq-dev \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    pkg-config

RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["sh", "-c", "python manage.py qcluster & python manage.py runserver 0.0.0.0:80"]
