FROM python:3.11
LABEL maintainer="Jonathan Hanson <jonathan@jonathan-hanson.org>"

WORKDIR /usr/src/app

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
        curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade \
    'pip' \
    'setuptools' \
    'wheel' \
    'paho-mqtt'

RUN curl -O https://raw.githubusercontent.com/merbanan/rtl_433/master/examples/rtl_433_mqtt_hass.py

COPY start_rtl_433_mqtt_hass.sh ./

CMD ["bash", "./start_rtl_433_mqtt_hass.sh"]
