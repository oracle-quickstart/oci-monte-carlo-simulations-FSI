# FSI Monte Carlo Simulator
FSI Monte Carlo simulator is a container based and cloud native solution that allow users to price European Vanilla Options through a Python-C++ wrapper. The solution is completelly compiled and containerized in order to easy the deployment.

## Prerequisites
To deploy the FSI Monte Carlo simulator you need to have an OCI OKE cluster deployed and running within any intel available shape. 

Tested shapes:

    VM.Standard.*
    BM.HPC.*
    
Considering to access the cluster for monitoring, configuring and testing from you laptop, OKE cluster should be deployed within public API endpoint and workers in private mode.

In order to start the deployment, you need to access to the OKE cluster through your Clud Shell Access and copy inside the configuration files:

* [ks8-deployment](ks8-deployment)

## Deploy
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


We now need to initialize the directory with the module in it.  This makes the module aware of the OCI provider.  You can do this by running:

    terraform init

This gives the following output:

![](./images/02%20-%20terraform%20init.png)

## Deploy
Now for the main attraction.  Let's make sure the plan looks good:

    terraform plan

You'll be prompted to enter a value for `var.adminPassword` if you haven't set a default in [variables.tf](./simple/variables.tf). That gives:

![](./images/03%20-%20terraform%20plan.png)

If that's good, we can go ahead and apply the deploy:

    terraform apply

You'll need to enter `yes` when prompted.  The apply should take about seven minutes to run.  Once complete, you'll see something like this:

![](./images/04%20-%20terraform%20apply.png)

When the apply is complete, the infrastructure will be deployed, but cloud-init scripts will still be running.  Those will wrap up asynchronously.  So, it'll be a few more minutes before your cluster is accessible.  Now is a good time to get a coffee.

## Connect to the Cluster
When the `terraform apply` completed, it printed out two values.  One of those is the URL to access Couchbase Server, the other one is for Couchbase Sync Gateway.  First, let's try accessing Server on port 8091 of the public IP.  You should see this:

![](./images/05%20-%20server%20login.png)

Now enter in the username (default `couchbase`) and password you specified in [variables.tf](./simple/variables.tf), or the value you entered when prompted if not defined in the file.  You should now have a view of your cluster and the services running.

![](./images/06%20-%20server.png)

Couchbase runs the admin interface on every node.  So, we could login to any node in the cluster to see this view.

Next, let's access to Sync Gateway on port 4984 of its public IP.  You should see:

![](./images/07%20-%20sync%20gateway.png)

## SSH to a Node
These machines are using Oracle Enterprise Linux (OEL).  The default login is opc.  You can SSH into the machine with a command like this:

    ssh -i ~/.ssh/oci opc@<Public IP Address>

Couchbase is installed under `/opt/couchbase/bin`.  You can debug deployments by investigating the cloud-init log file `/var/log/messages`.  You'll need to `sudo su` to be able to read it.

![](./images/08%20-%20ssh.png)

## View the Cluster in the Console
You can also login to the web console [here](https://console.us-phoenix-1.oraclecloud.com/a/compute/instances) to view the IaaS that is running the cluster.

![](./images/09%20-%20console.png)

## Destroy the Deployment
When you no longer need the deployment, you can run this command to destroy it:

    terraform destroy

You'll need to enter `yes` when prompted.  Once complete, you'll see something like this:

![](./images/10%20-%20terraform%20destroy.png)
