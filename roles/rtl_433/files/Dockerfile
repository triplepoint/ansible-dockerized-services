FROM python:3.12
LABEL maintainer="Jonathan Hanson <jonathan@jonathan-hanson.org>"

WORKDIR /usr/src/app

RUN pip install --no-cache-dir --upgrade \
    'pip' \
    'setuptools' \
    'wheel' \
    'paho-mqtt'

ARG RTL_433_VERSION

ADD https://raw.githubusercontent.com/merbanan/rtl_433/$RTL_433_VERSION/examples/rtl_433_mqtt_hass.py ./
COPY start_rtl_433_mqtt_hass.sh ./

CMD ["bash", "./start_rtl_433_mqtt_hass.sh"]
