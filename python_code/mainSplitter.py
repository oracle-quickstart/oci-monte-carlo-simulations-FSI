import os, runSplitter
print("RabbitMQHost = " + os.environ['RABBITMQ_HOST'])
print("RabbitMQQueue = " + os.environ['RABBITMQ_TASKQUEUE'])
print("RabbitMQQueueSplittable = " + os.environ['RABBITMQ_TASKQUEUE_SPLITTABLE'])
print("RabbitMQPrefetch = " + os.environ['RABBITMQ_PREFETCHCOUNT'])
print("MinSimulations = " + os.environ['NUM_STEPS'])
runSplitter.splitter()
