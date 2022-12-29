FROM python:3.11
LABEL maintainer="Jonathan Hanson <jonathan@jonathan-hanson.org>"

WORKDIR /usr/src/app

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
        curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade \
    'pip' \
    'pipenv' \
    'setuptools' \
    'wheel'

COPY Pipfile ./
COPY Pipfile.lock ./

RUN pipenv install --deploy

COPY start_rtl_433_mqtt_hass.sh ./

RUN curl -O https://raw.githubusercontent.com/triplepoint/rtl_433/master/examples/rtl_433_mqtt_hass.py

CMD ["bash", "./start_rtl_433_mqtt_hass.sh"]
