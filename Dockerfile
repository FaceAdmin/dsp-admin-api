# 1) Берём базу с Miniforge (conda-forge, ARM‑ready)
FROM condaforge/miniforge3:latest

# 2) Рабочая папка
WORKDIR /app

# 3) Копируем environment и создаём conda‑окружение
COPY environment.yml .
RUN mamba env create -f environment.yml \
 && mamba clean --all -y

# 4) Делаем shell внутри этого окружения
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-lc"]

# 5) Копируем ваш code & статические файлы
COPY . .

# 6) Собираем статику, миграции и т.д. (если нужно)
RUN python manage.py collectstatic --noinput \
 && python manage.py migrate

# 7) Экспонируем порт
EXPOSE 80

# 8) Запуск qcluster + dev‑сервер
CMD python manage.py qcluster & \
    python manage.py runserver 0.0.0.0:80
