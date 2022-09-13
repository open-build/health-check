# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.11-rc-slim

# Add user that will be used in the container.
RUN useradd builder

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Install system packages required by Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    libmariadb-dev-compat \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    python3-dev \
    default-libmysqlclient-dev \
    default-mysql-client \
    build-essential \
    redis-server \
    celery \
    sudo \
    supervisor \
    cron \
 && rm -rf /var/lib/apt/lists/*

# Fix permissions on crontab
RUN chmod u=rwx,g=wxs,o=t /var/spool/cron/crontabs

# Install the application server.
RUN pip3 install "gunicorn==20.0.4"

# Install the project requirements.
COPY requirements.txt /
RUN pip3 install -r /requirements.txt

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set this directory to be owned by the "builder" user.
RUN chown builder:builder /app

# Copy the source code of the project into the container.
COPY --chown=builder:builder . .

# MAKE MIGRATIONS
RUN python3 manage.py makemigrations

# Use user "builder" to run the build commands below and the server itself.
USER builder

# Collect static files.
CMD python3 manage.py collectstatic --noinput --clear

# Runtime command that executes when "docker run" is called, it does the
# following:
#   1. Migrate the database.
#   2. Start the application server.
# WARNING:
#   Migrating database at the same time as starting the server IS NOT THE BEST
#   PRACTICE. The database should be migrated manually or using the release
#   phase facilities of your hosting platform. This is used only so the
#   instance can be started with a simple "docker run" command.
CMD set -xe; python3 manage.py migrate --noinput --database; gunicorn mysite.wsgi:application
