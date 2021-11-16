#!/bin/bash

if [ "$1" == "light" ]
then
  kubectl delete replicationcontroller intel-worker-controller
  kubectl delete replicationcontroller intel-splitter-controller
  kubectl delete replicationcontroller intel-client-controller
  kubectl delete replicationcontroller arm-worker-controller
  kubectl delete replicationcontroller arm-splitter-controller
  kubectl delete replicationcontroller arm-client-controller
else
  if [ "$1" == "all" ]
  then
    kubectl delete replicationcontroller rabbitmq-controller
    kubectl delete replicationcontroller intel-worker-controller
    kubectl delete replicationcontroller intel-splitter-controller
    kubectl delete replicationcontroller intel-client-controller
    kubectl delete replicationcontroller arm-worker-controller
    kubectl delete replicationcontroller arm-splitter-controller
    kubectl delete replicationcontroller arm-client-controller
    kubectl delete replicationcontroller splunk-controller
    kubectl delete service loadbalancer
    kubectl delete service rabbitmq-service
    kubectl delete service splunk-service
  else
    echo "Please, follow the instructions and include light or all to select the stop mode"
  fi
fi
