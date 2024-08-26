# Set the python version as a build-time argument
# with Python 3.12 as the default
ARG PYTHON_VERSION=3.11-slim-bullseye
FROM python:${PYTHON_VERSION}

# Create a virtual environment
RUN python -m venv /opt/venv

# Set the virtual environment as the current location
ENV PATH=/opt/venv/bin:$PATH

# Upgrade pip
RUN pip install --upgrade pip

# Install pipenv
RUN pip install pipenv

# Set Python-related environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install os dependencies for our mini vm
RUN apt-get update && apt-get install -y \
    # for postgres
    libpq-dev \
    # for Pillow
    libjpeg-dev \
    # for CairoSVG
    libcairo2 \
    # other
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create the mini vm's code directory
RUN mkdir -p /code

# Set the working directory to that same code directory
WORKDIR /code

# Copy the Pipfile and Pipfile.lock into the container
COPY Pipfile Pipfile.lock /code/

# Install the Python project dependencies using pipenv
RUN pipenv install --python /opt/venv/bin/python --deploy --ignore-pipfile

# Copy the project code into the container's working directory
COPY ./src /code

# database isn't available during build
ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}

# ARG DJANGO_DEBUG=0
# ENV DJANGO_DEBUG=${DJANGO_DEBUG}

ARG ENVIRONMENT="production"
ENV ENVIRONMENT=${ENVIRONMENT}
# run any other commands that do not need the database
# such as:
# RUN pipenv run python manage.py vendor_pull
RUN pipenv run python manage.py collectstatic --noinput
# RUN pipenv run python manage.py collectstatic --noinput

# set the Django default project name
ARG PROJ_NAME="config"

# create a bash script to run the Django project
# this script will execute at runtime when
# the container starts and the database is available
RUN printf "#!/bin/bash\n" > ./paracord_runner.sh && \
    printf "RUN_PORT=\"\${PORT:-8000}\"\n\n" >> ./paracord_runner.sh && \
    printf "pipenv run python manage.py migrate --no-input\n" >> ./paracord_runner.sh && \
    printf "pipenv run gunicorn ${PROJ_NAME}.wsgi:application --bind \"0.0.0.0:\$RUN_PORT\"\n" >> ./paracord_runner.sh

# make the bash script executable
RUN chmod +x paracord_runner.sh

# Clean up apt cache to reduce image size
RUN apt-get remove --purge -y \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Run the Django project via the runtime script
# when the container starts
CMD ./paracord_runner.sh