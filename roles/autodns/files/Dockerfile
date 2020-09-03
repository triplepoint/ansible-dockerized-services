FROM python:3.8
LABEL maintainer="Jonathan Hanson <jonathan@jonathan-hanson.org>"

ARG UID_GID=1085

RUN addgroup --gid $UID_GID app \
    && adduser --uid $UID_GID --gid $UID_GID --system --disabled-password --disabled-login app

VOLUME ["/home/app/.aws"]
VOLUME ["/etc/update_route53"]
VOLUME ["/var/log/update_route53"]

WORKDIR /usr/src/app

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
        dnsutils \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade \
    pip \
    pipenv \
    setuptools<50 \
    wheel

COPY Pipfile ./
COPY Pipfile.lock ./

USER app

RUN pipenv install --deploy

COPY update_route53.sh ./

CMD ["pipenv", "run", "bash", "./update_route53.sh"]
