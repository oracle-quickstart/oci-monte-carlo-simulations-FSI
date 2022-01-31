## EVITAR TRUNCADO DE DATOS AL ENVIAR AL HEC:
# https://community.splunk.com/t5/Getting-Data-In/http-event-collector-truncates-event-to-10-000-characters/m-p/509378
# /opt/splunk/bin/splunk btool props list _json --debug | grep -i truncate
# /opt/splunk/etc/system/default/props.conf TRUNCATE = 10000000

## EVITAR TRUNCADO DE DATOS EN EL mvexpand
# vi /opt/splunk/etc/system/default/limits.conf
# [mvexpand]
# max_mem_usage_mb = 30720
# max_mem_usage_mb = 100000

## Para incluir un nuevo fichero en la imagen (ej: props.conf)
# Editar el Dockerfile de la ruta: docker-splunk-develop/splunk/common-files/Dockerfile

## Para realizar una llamada dentro del contenedor a su inicio
# Editar el fichero: docker-splunk-develop/splunk/common-files/entrypoint.sh

## Ejecucion del contenedor en maquina de compilacion
docker run -d -p 8000:8000 -e "SPLUNK_PASSWORD=password" -e "SPLUNK_START_ARGS=--accept-license" -it --name so2 splunk-redhat-8:latest

## Documentacion de la construccion del contenedor redhad based
https://splunk.github.io/docker-splunk/ADVANCED.html#configure-splunk

## Ruta de copiado del dashboard: apps/search/local/data/ui/views/cacahuete.xml
## Acceso al dashboard: http://150.136.4.128:8000/en-US/app/search/cacahuete