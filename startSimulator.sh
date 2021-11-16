#!/bin/bash

#var=""

#if [ "$1" == "all" ]
#then
#  var="all_architectures"
#fi

echo "Deploying OCI FSI Monte Carlo Simulator"

kubectl create -f ks8-deployment/all_architectures/storageClass.yaml
kubectl create -f ks8-deployment/all_architectures/persistentVolume.yaml
kubectl create -f ks8-deployment/all_architectures/persistentVolumeClaim.yaml
kubectl create -f ks8-deployment/all_architectures/splunk-controller.yaml
kubectl create -f ks8-deployment/all_architectures/splunk-service.yaml
echo "Reporting tool deployed"

kubectl create -f ks8-deployment/all_architectures/rabbitmq-controller.yaml
kubectl create -f ks8-deployment/all_architectures/rabbitmq-service.yaml
echo "RabbitMQ deployed"
kubectl create -f ks8-deployment/all_architectures/loadbalancer-service.yaml
echo "LoadBalancer deployed"
sleep 15

kubectl create -f ks8-deployment/all_architectures/intel-worker-controller.yaml
kubectl create -f ks8-deployment/all_architectures/intel-splitter-controller.yaml
kubectl create -f ks8-deployment/all_architectures/intel-client-controller.yaml
kubectl create -f ks8-deployment/all_architectures/arm-worker-controller.yaml
kubectl create -f ks8-deployment/all_architectures/arm-splitter-controller.yaml
kubectl create -f ks8-deployment/all_architectures/arm-client-controller.yaml


echo "Monte Carlo Simulator core deployed"
