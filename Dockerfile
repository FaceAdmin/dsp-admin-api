# ——— Стадия 1. Сборка колёс ———
FROM python:3.11-slim AS builder
WORKDIR /app

# 1. Системные зависимости для сборки dlib
RUN apt update && apt install -y --no-install-recommends \
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
      pkg-config \
 && rm -rf /var/lib/apt/lists/*

# 2. Параллельно используем все 4 ядра
ENV MAKEFLAGS="-j$(nproc)"

# 3. Апгрейд pip и создание заранее всех wheel-файлов
RUN pip install --upgrade pip setuptools wheel
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt


# ——— Стадия 2. Лёгкий продакшн-образ ———
FROM python:3.11-slim
WORKDIR /app

# 1. Библиотеки, нужные только во время рантайма (без dev‑пакетов)
RUN apt update && apt install -y --no-install-recommends \
      libpq-dev \
      libopenblas-dev \
      liblapack-dev \
      libx11-6 \
      libgtk-3-0 \
 && rm -rf /var/lib/apt/lists/*

# 2. Берём уже собранные wheel‑файлы и ставим их без интернета
COPY --from=builder /wheels /wheels
RUN pip install --no-index --find-links=/wheels \
      face_recognition \
      numpy \
      Django \
      djangorestframework \
      psycopg2 \
      PyJWT \
      pyotp \
      qrcode[pil] \
      sendgrid \
      sendgrid-django \
      django-cryptography \
      django-q \
      django-environ \
      django-cors-headers

# 3. Копируем код и указываем команду запуска
COPY . .
CMD ["sh", "-c", "python manage.py qcluster & python manage.py runserver 0.0.0.0:80"]
