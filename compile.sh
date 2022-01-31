if [ "$1" == "arm" ]
then
	docker build -t iad.ocir.io/hpc_limited_availability/arm-worker:latest --no-cache -f docker/worker-dockerfile .
        docker build -t iad.ocir.io/hpc_limited_availability/arm-splitter:latest --no-cache -f docker/splitter-dockerfile .
	docker build -t iad.ocir.io/hpc_limited_availability/arm-client:latest --no-cache -f docker/client-dockerfile .
	
	docker push iad.ocir.io/hpc_limited_availability/arm-worker:latest
        docker push iad.ocir.io/hpc_limited_availability/arm-splitter:latest
        docker push iad.ocir.io/hpc_limited_availability/arm-client:latest
	
else
        if [ "$1" == "intel" ]
        then
        	docker build -t iad.ocir.io/hpc_limited_availability/intel-worker:latest --no-cache -f docker/worker-dockerfile .
		docker build -t iad.ocir.io/hpc_limited_availability/intel-splitter:latest --no-cache -f docker/splitter-dockerfile .
		docker build -t iad.ocir.io/hpc_limited_availability/intel-client:latest --no-cache -f docker/client-dockerfile .

	        docker push iad.ocir.io/hpc_limited_availability/intel-worker:latest
        	docker push iad.ocir.io/hpc_limited_availability/intel-splitter:latest
        	docker push iad.ocir.io/hpc_limited_availability/intel-client:latest
		
		cd splunk/docker-splunk-develop
		make splunk-redhat-8
		docker tag splunk-redhat-8:latest iad.ocir.io/hpc_limited_availability/splunk:latest		
		docker push iad.ocir.io/hpc_limited_availability/splunk:latest

		docker pull rabbitmq:3-management
		docker tag rabbitmq:3-management iad.ocir.io/hpc_limited_availability/rabbitmq:latest
		docker push iad.ocir.io/hpc_limited_availability/rabbitmq:latest
	else
		echo "Please, select arm or intel compilation"
        fi
fi
