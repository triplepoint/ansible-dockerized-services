FROM python:3.11
LABEL maintainer="Jonathan Hanson <jonathan@jonathan-hanson.org>"

VOLUME ["/root/.aws"]
VOLUME ["/etc/update_route53"]
VOLUME ["/var/log/update_route53"]

WORKDIR /usr/src/app

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
        dnsutils \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade \
    'pip' \
    'setuptools' \
    'wheel' \
    'awscli'

COPY update_route53.sh ./

CMD ["bash", "./update_route53.sh"]
