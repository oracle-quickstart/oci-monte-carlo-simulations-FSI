#!/bin/bash

var = ""

if [ $1 == "all" ]
then
  var = "all_architectures"
else
  var = "intel"
fi

echo "Deploying OCI FSI Monte Carlo Simulator"

kubectl create -f ks8-deployment/$var/storageClass.yaml
kubectl create -f ks8-deployment/$var/persistentVolume.yaml
kubectl create -f ks8-deployment/$var/persistentVolumeClaim.yaml
kubectl create -f ks8-deployment/$var/splunk-controller.yaml
kubectl create -f ks8-deployment/$var/splunk-service.yaml
echo "Reporting tool deployed"

kubectl create -f ks8-deployment/$var/rabbitmq-controller.yaml
kubectl create -f ks8-deployment/$var/rabbitmq-service.yaml
echo "RabbitMQ deployed"
kubectl create -f ks8-deployment/$var/loadbalancer-service.yaml
echo "LoadBalancer deployed"
sleep 15

kubectl create -f ks8-deployment/$var/mcv-controller.yaml
kubectl create -f ks8-deployment/$var/mcv-parent-controller.yaml
kubectl create -f ks8-deployment/$var/mcv-client-controller.yaml
echo "Monte Carlo Simulator core deployed"




