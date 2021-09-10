# FSI Monte Carlo Simulator
FSI Monte Carlo simulator is a container based and cloud native solution that allow users to price European Vanilla Options through a Python-C++ wrapper. The solution is completelly compiled and containerized in order to easy the deployment.

## Prerequisites
To deploy the FSI Monte Carlo simulator you need to have an OCI OKE cluster deployed and running within any intel available shape. 

Tested shapes:

    VM.Standard.*
    BM.HPC.*
    
Considering to access the cluster for monitoring, configuring and testing from you laptop, OKE cluster should be deployed within public API endpoint and workers in private mode.

To enable the detailed monitoring, you need to set a file system and a mount target created according to the instructions in [Announcing File Storage Service UI 2.0](https://blogs.oracle.com/cloud-infrastructure/post/announcing-file-storage-service-ui-20)

Please, do not forget to set up the security list for the FSS:
![](https://github.com/oracle-quickstart/oci-monte-carlo-simulations-FSI/blob/main/images/security_list_fss.png)

In order to start the deployment, you need to access to the OKE cluster through your Cloud Shell Access and clone the FSI Monte Carlo Simulator github repository and set the permission for the installation script:

    git clone https://github.com/oracle-quickstart/oci-monte-carlo-simulations-FSI.git
    chmod +x oci-monte-carlo-simulations-FSI/install.sh
    cd oci-monte-carlo-simulations-FSI/
    ./install.sh


## Deployment process (install.sh script)
Based on the architecture, first deployment step is to run the RabbitMQ node:

    kubectl create -f rabbitmq-controller.yaml

Once created the controller, you need to deploy the RabbitMQ services that will allow you to identify the node by FQDN and solve possible issues with the ip rotation:

    kubectl create -f rabbitmq-service.yaml

Now, your RabbitMQ host will be reacheble through "rabbitmq-service".
By default, ports in the private subnet are not opened so, you need to set the rules in the security list to allow the communication through port 5672 fron the rest of nodes in this subnet.

After that, we are setting the configuration to enable the access to the RabbitMQ WEB GUI in port 15672 and 5672 to send the valuations from out laptop. First step is to deploy the loadbalancer service that will allow foreing access through the public subnet.

    kubectl create -f loadbalancer-service.yaml

One more time, you need to ensure that the firewall rules are correctly configured on the public security list for ports 15672 and 5672.

Ready to deploy the Monte Carlo Vanilla containers, they will automatically connect to the RabbitMQ host (var RABBITMQ_HOST=rabbitmq-service).

    kubectl create -f mcv-controller.yaml

mcv-controller will deploy 100 pods over the node pool selected. Please, to increase the performance, ensure to set the number of pods according to the number of OCPUs in your node pool. You can scale the number of pods with:

    kubectl scale --replicas=[NUM_OF_REPLICAS] rc/mcv-controller

After that, this client will include all the connectors and input files required to test the solution:

    kubectl create -f mcv-client-controller.yaml

The solution is completelly deployed, please check that the RabbitMQ host is running accessing through the WEB GUI and all mcv-controller consumers must be connected to the tasks_in queue.

### Access your RabbitMQ Management GUI
Run the next command to list the load balancer service to get the public IP:

    kubectl get services | grep loadbalancer

![](https://github.com/oracle-quickstart/oci-monte-carlo-simulations-FSI/blob/main/images/loadbalancer_publicip.png)

You can reach the RabbitMQ Management GUI: loadbalancer_publicip:15672

### Access your Splunk Management GUI
You can reach the RabbitMQ Management GUI: loadbalancer_publicip:8000

## SSH to the client
In order to test the simulator, first of all you need to identify the name of the client pod:

    kubectl get pods | grep mcv-client-controller

Once identified the name of the pod, you can access to inside running:

    kubectl exec --stdin --tty [CLIENT_POD_NAME] -- /bin/bash

## Testing
Inside the client pod, you can find these portfolio examples to be used as input files:

* [simulations.json](input-files/simulations.json) --> 2 simple deals
* [simulation_50_simple.json](input-files/simulation_50_simples.json) --> 50 simple deals
* [simulation_1000_simple.json](input-files/simulation_1000_simple.json) --> 1000 simple deals
* [simulation_30000_simple.json](input-files/simulation_30000_simple.json) --> 30000 simple deals

All of them are complex portfolios (build with more than one deal). Internally, each portfolio can include simple.

To run the client and start the calculation:

    python3 main.py [INPUTFILE]

## Simple or complex deal examples
Simple deal means that number of Monte Carlo simulations will be 3.000.000 or less and won't be splitable

    {
    "portfolio_id": 1000,
    "parent_id": 0,
    "child_id": 0,
    "level": 0,
    "num_sims": 3000000,
    "underlying": 102,
    "strike": 102,
    "riskfreerate": 0.02,
    "volatility": 0.01,
    "maturity": 1,
    "exec_time": 0
    }

## Results
Theroretical time of one simple task (3.000.000 Monte Carlo simulations), based on BM.HPC2.36 shape, takes 0,510ms. Simulator time is 0,523s approx.

## Destroy the simulator
When you no longer need the deployment, you can delete the OKE cluster
