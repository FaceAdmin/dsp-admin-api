FROM python:3.10-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
      build-essential \
      cmake \
      pkg-config \
      libx11-dev \
      libatlas-base-dev \
      libgtk-3-dev \
      libboost-python-dev \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /tmp/dlib-src \
&& cd /tmp/dlib-src \
&& pip download dlib==19.24.2 --no-binary=:all: \
&& tar xzf dlib-19.24.2.tar.gz \
&& sed -i 's/cmake_minimum_required(VERSION 2.8)/cmake_minimum_required(VERSION 3.5)/g' dlib-19.24.2/dlib/external/pybind11/CMakeLists.txt \
&& cd dlib-19.24.2 \
&& python setup.py bdist_wheel \
&& pip install dist/*.whl \
&& rm -rf /tmp/dlib-src

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel \
 && pip install -r requirements.txt

COPY . .
CMD ["sh", "-c", "python manage.py qcluster & python manage.py runserver 0.0.0.0:80"]
