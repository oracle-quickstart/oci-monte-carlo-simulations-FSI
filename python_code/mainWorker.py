import os, runWorker
print("RabbitMQHost = " + os.environ['RABBITMQ_HOST'])
print("RabbitMQQueue = " + os.environ['RABBITMQ_TASKQUEUE'])
print("RabbitMQPrefetch = " + os.environ['RABBITMQ_PREFETCHCOUNT'])
print("MinSimulations = " + os.environ['NUM_STEPS'])
runWorker.splitter()
