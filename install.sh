echo "Deploying OCI FSI Monte Carlo Simulator"

kubectl create -f ks8-deployment/storageClass.yaml
kubectl create -f ks8-deployment/persistentVolume.yaml
kubectl create -f ks8-deployment/persistentVolumeClaim.yaml
kubectl create -f ks8-deployment/splunk-controller.yaml
kubectl create -f ks8-deployment/splunk-service.yaml
echo "Reporting tool deployed"

kubectl create -f ks8-deployment/rabbitmq-controller.yaml
kubectl create -f ks8-deployment/rabbitmq-service.yaml
echo "RabbitMQ deployed"
kubectl create -f ks8-deployment/loadbalancer-service.yaml
echo "LoadBalancer deployed"
sleep 15

kubectl create -f ks8-deployment/mcv-controller.yaml
kubectl create -f ks8-deployment/mcv-parent-controller.yaml
kubectl create -f ks8-deployment/mcv-client-controller.yaml
echo "Monte Carlo Simulator core deployed"




