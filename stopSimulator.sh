#!/bin/bash

if [ "$1" == "light" ]
then
  kubectl delete replicationcontroller mcv-controller
  kubectl delete replicationcontroller mcv-parent-controller
  kubectl delete replicationcontroller mcv-client-controller
else
  kubectl delete replicationcontroller rabbitmq-controller
  kubectl delete replicationcontroller mcv-controller
  kubectl delete replicationcontroller mcv-parent-controller
  kubectl delete replicationcontroller mcv-client-controller
  kubectl delete replicationcontroller splunk-controller
  kubectl delete service loadbalancer
  kubectl delete service rabbitmq-service
  kubectl delete service splunk-service
fi
