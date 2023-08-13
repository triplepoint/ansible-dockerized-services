python3 -u ./rtl_433_mqtt_hass.py --host ${MQTT_HOST} --port ${MQTT_PORT} --ca_cert ${MQTT_CA_CERT_PATH} \
  --rtl-topic ${RTL_TOPIC} --discovery-prefix ${DISCOVERY_PREFIX} --device-topic_suffix ${DEVICE_TOPIC_SUFFIX} \
  --interval ${DISCOVERY_INTERVAL} ${OTHER_ARGS}
