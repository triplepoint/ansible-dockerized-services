FROM python:3.8
LABEL maintainer="Jonathan Hanson <jonathan@jonathan-hanson.org>"

# TODO VOLUME ["whatever we're doing about the AWS credentials file"]
VOLUME ["/etc/update_route53"]
VOLUME ["/var/log/update_route53"]

WORKDIR /usr/src/app

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
      dnsutils \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade \
    pip \
    pipenv \
    setuptools \
    wheel

COPY Pipfile ./
COPY Pipfile.lock ./

RUN pipenv install --deploy

COPY update_route53.sh ./
RUN chmod 0755 update_route53.sh

CMD ["/usr/local/bin/pipenv", "run", "./update_route53.sh", ">", "/proc/1/fd/1", "2>/proc/1/fd/2"]
