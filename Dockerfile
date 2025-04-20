FROM condaforge/mambaforge:latest
WORKDIR /app

# создаём окружение и ставим нужные пакеты из conda-forge
COPY environment.yml .
RUN mamba env create -f environment.yml && mamba clean --all -y

# далее работаем внутри env
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-lc"]

COPY requirements.txt .
# pip ставит только остальные зависимости, dlib уже есть в conda
RUN pip install --no-deps -r requirements.txt

COPY . .
CMD ["conda", "run", "-n", "myenv", "bash", "-lc", 
     "python manage.py qcluster & python manage.py runserver 0.0.0.0:80"]
