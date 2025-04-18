FROM python:3.11-slim
WORKDIR /app

RUN apt update && apt upgrade -y && apt install -y pkg-config build-essential gcc libpq-dev

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD [ "python", "manage.py", "qcluster", "&&", "python", "manage.py", "runserver", "0.0.0.0:80" ]
