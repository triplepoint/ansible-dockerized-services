FROM python:3.9
LABEL maintainer="Jonathan Hanson <jonathan@jonathan-hanson.org>"

WORKDIR /usr/src/app

RUN pip install --no-cache-dir --upgrade \
    'pip' \
    'pipenv' \
    'setuptools' \
    'wheel'

COPY Pipfile ./
COPY Pipfile.lock ./

RUN pipenv install --deploy

COPY start_rtl_433_mqtt_hass.sh ./
COPY rtl_433_mqtt_hass.py ./

CMD ["bash", "./start_rtl_433_mqtt_hass.sh"]
