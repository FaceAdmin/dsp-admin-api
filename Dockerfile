FROM python:3.10-slim
WORKDIR /app

RUN apt update && apt install -y \
      build-essential \
      cmake \             
      make \               
      ninja-build \        
      python3-dev \     
      libpq-dev \       
      libopenblas-dev \
      liblapack-dev \
      libx11-6 \
      libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel \
 && pip install -r requirements.txt

COPY . .
CMD ["sh", "-c", "python manage.py qcluster & python manage.py runserver 0.0.0.0:80"]
