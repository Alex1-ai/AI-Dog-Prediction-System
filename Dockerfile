FROM python:3.11.4-slim-bullseye

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .


RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "app.wsgi:application", "--config", "gunicorn.conf.py"]
