FROM ubuntu:noble

RUN apt-get update -qqy \
  && apt-get -qqy --no-install-recommends install \
    python3.12 python3.12-venv python3.12-dev pkg-config libmysqlclient-dev \
    build-essential && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/*


RUN mkdir -p /srv/app-management/app
RUN chown -R ubuntu:ubuntu /srv/app-management

USER ubuntu

RUN python3.12 -m venv /srv/app-management/env
RUN /srv/app-management/env/bin/python -m pip install --upgrade pip setuptools wheel

ENV PATH="/srv/app-management/env/bin:${PATH}"
WORKDIR /srv/app-management/app

COPY requirements.txt /srv/app-management/app/requirements.txt
RUN /srv/app-management/env/bin/python -m pip install --no-cache-dir -r /srv/app-management/app/requirements.txt

COPY --chown=ubuntu . /srv/app-management/app
