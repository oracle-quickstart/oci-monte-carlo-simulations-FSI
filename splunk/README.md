# FSI Monte Carlo Simulator - Splunk configuration

## How to avoid data trucation in HEC:
Splunk documentation: ![](https://community.splunk.com/t5/Getting-Data-In/http-event-collector-truncates-event-to-10-000-characters/m-p/509378)
Edit file: docker-splunk-develop/props.conf and set:

    TRUNCATE = 10000000

## How to avoid data trucation when running mvexpand:
Edit file: docker-splunk-develop/limits.conf and set:

    [mvexpand]
    max_mem_usage_mb = 30720
    max_mem_usage_mb = 100000

## How to include new configuration files in Splunk image (example: props.conf)
Edit file: docker-splunk-develop/splunk/common-files/Dockerfile and set new add files

## How to include new commands on container ejecution entrypoint
Edit file: docker-splunk-develop/splunk/common-files/entrypoint.sh

## Container build documentation
https://splunk.github.io/docker-splunk/ADVANCED.html#configure-splunk
