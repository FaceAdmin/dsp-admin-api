FROM condaforge/miniforge3:latest

WORKDIR /app

COPY environment.yml .
RUN mamba env create -f environment.yml \
 && mamba clean --all -y

SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-lc"]

COPY . .

EXPOSE 80

CMD python manage.py qcluster & \
    python manage.py runserver 0.0.0.0:80
