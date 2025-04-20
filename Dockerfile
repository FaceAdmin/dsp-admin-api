FROM python:3.10-slim

WORKDIR /app

# Только лёгкие рантайм‑зависимости (BLAS, Postgres client и т.п.)
RUN apt update && apt install -y --no-install-recommends \
      libpq-dev \
      libopenblas-dev \
      liblapack-dev \
      libx11-6 \
      libgtk-3-0 \
      gcc \
      cmake \
    && rm -rf /var/lib/apt/lists/*

# Апгрейд pip и установка всех пакетов
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel \
 && pip install --only-binary=:all: -r requirements.txt

COPY . .

# Запускаем воркер и сервер параллельно
CMD ["sh", "-c", "python manage.py qcluster & python manage.py runserver 0.0.0.0:80"]
