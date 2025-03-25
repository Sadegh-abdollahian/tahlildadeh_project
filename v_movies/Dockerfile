FROM python:3.10

WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    libdbus-1-dev \
    gettext \
    locales \
    cmake \
    libgirepository1.0-dev \
    librsync-dev \
    libcups2-dev \
    && rm -rf /var/lib/apt/lists/*

# Set up locales
RUN locale-gen en_US.UTF-8 && dpkg-reconfigure locales

COPY requirements.txt /code/

RUN pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

EXPOSE 8000

CMD ["gunicorn", "v_movies.wsgi", "-b", "0.0.0.0:8000"]
