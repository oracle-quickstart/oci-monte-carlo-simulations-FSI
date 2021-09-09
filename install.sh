./kubectl create -f ks8-deployment/rabbitmq-controller.yaml
./kubectl create -f ks8-deployment/rabbitmq-service.yaml
./kubectl create -f ks8-deployment/loadbalancer-service.yaml
./kubectl create -f ks8-deployment/mcv-controller.yaml
./kubectl create -f ks8-deployment/mcv-client-controller.yaml
./kubectl create -f ks8-deployment/mcv-parent-controller.yaml

#./kubectl create -f oci-monte-carlo-simulations-FSI/ks8-deployment/splunk-controller.yaml
#./kubectl create -f oci-monte-carlo-simulations-FSI/ks8-deployment/splunk-service.yaml
#git clone https://github.com/oracle-quickstart/oci-monte-carlo-simulations-FSI.git
