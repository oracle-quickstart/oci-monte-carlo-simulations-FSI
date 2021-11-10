#!/bin/bash

if [ "$1" == "light" ]
then
  kubectl delete replicationcontroller mcv-controller
  kubectl delete replicationcontroller mcv-parent-controller
  kubectl delete replicationcontroller mcv-client-controller
else
  if [ "$1" == "all" ]
  then
    kubectl delete replicationcontroller rabbitmq-controller
    kubectl delete replicationcontroller mcv-controller
    kubectl delete replicationcontroller mcv-parent-controller
    kubectl delete replicationcontroller mcv-client-controller
    kubectl delete replicationcontroller splunk-controller
    kubectl delete service loadbalancer
    kubectl delete service rabbitmq-service
    kubectl delete service splunk-service
  else
    echo "Please, follow the instructions and include light or all to select the stop mode"
  fi
fi
