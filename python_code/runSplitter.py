import os, json, pika, random, threading
from datetime import datetime
import numpy as np
from io import StringIO

class splitter:
    channel_consumer_splittable = ""
    channel_consumer_parent = ""
    channel_producer = ""
    channel_producer_final = ""
    connection1 = ""
    connection2 = ""
    connection3 = ""
    total_tasks = 0
    portfolio_id = ""
    parent_result = ""
    callback_count = 0

    def to_nparray(self, string):
        nparray = [[]]
        string = string.replace("],", "];").replace(" ", "").replace("'", "").replace("[[", "[").replace("]]", "]").replace("[","").replace("]","")
        aux_array = string.split(";")
        for i in aux_array:
            aux = i.split(",")
            itera = []
            for k in aux:
                itera = np.append(itera, float(k))
            if nparray == []:
                nparray = itera
            else:
                nparray = np.append(nparray, itera)
        return nparray

    def callback_parent(self, ch, method, properties, body):
        data = eval(body)
        self.callback_count = self.callback_count + 1
        if (self.parent_result == ""):
            self.parent_result = data
        else:
            if (datetime.strptime(data["exec_time"], '%H:%M:%S.%f') > datetime.strptime(self.parent_result["exec_time"], '%H:%M:%S.%f')):
                self.parent_result["exec_time"] = data["exec_time"]
            if (int(data["child_id"]) > int(self.parent_result["child_id"])):
                self.parent_result["child_id"] = data["child_id"]
            _paths = np.append(self.to_nparray(self.parent_result["paths"]), self.to_nparray(data["paths"]))
            self.parent_result["paths"] = str(_paths.tolist())
            self.parent_result["num_steps"] = int(self.parent_result["num_steps"]) + int(data["num_steps"])
            aux = str(self.parent_result["worker"])+","+str(data["worker"])
            _worker = {"worker": str(aux)}
            self.parent_result.update(_worker)
            if (self.callback_count == self.total_tasks):
                _paths = np.reshape(_paths, (-1, int(data["num_sims"])))
                _strike = float(self.parent_result["strike"])
                _riskfreerate = float(self.parent_result["riskfreerate"])
                _maturity = float(self.parent_result["maturity"])
                payoffs = np.maximum(_paths[-1]-_strike, 0)
                _option_price = np.mean(payoffs)*np.exp(-_riskfreerate*_maturity) #discounting back to present value
                _max=np.max(_paths,axis=0)
                option_price = {"option_price": str(_option_price)}
                paths = {"paths": str(_paths.tolist())}
                paths_max = {"paths_max": str(_max.tolist())}
                self.parent_result.update(option_price)
                self.parent_result.update(paths_max)
                self.parent_result.update(paths)
                self.connection3 = pika.BlockingConnection(pika.ConnectionParameters(os.environ['RABBITMQ_HOST']))
                self.channel_producer_final = self.connection3.channel()
                _queue_final = str(self.portfolio_id) + "_result"
                self.channel_producer_final.queue_declare(queue=_queue_final)
                _queue = str(self.portfolio_id) + "_result"
                _end_time = datetime.now()
                end_time = {"end_time": str(_end_time)}
                self.parent_result.update(end_time)
                _return = str(self.parent_result).replace("\'", "\\\"")
                _return = _return.replace("\\", "")
                self.channel_producer_final.basic_publish(exchange='', routing_key=_queue, body=str(_return))
                _queue_delete = str(self.portfolio_id) + "_" + str(data["parent_id"])
                self.channel_consumer_parent.queue_delete(queue=_queue_delete)
                self.total_tasks = 0
                self.callback_count = 0
                self.parent_result = ""
                self.connection3.close()          

    def callback(self, ch, method, properties, body):
        self.connection2 = pika.BlockingConnection(pika.ConnectionParameters(os.environ['RABBITMQ_HOST']))
        self.channel_consumer_parent = self.connection2.channel()
        self.channel_producer = self.connection2.channel()
        self.channel_producer.queue_declare(queue=os.environ['RABBITMQ_TASKQUEUE'], arguments={"x-max-priority": 10})
        data = eval(body)
        count = 0
        self.portfolio_id = ""
        _parent_id = ""
        for i in data:
            if (count == 0):
                self.portfolio_id = i["portfolio_id"]
            _min_steps = int(os.environ['NUM_STEPS'])
            _num_steps = i["num_steps"]
            _num_tasks = int(_num_steps / _min_steps)
            for n in range(_num_tasks):
                count = count + 1
                i["child_id"] = count
                i["level"] = 2
                i["num_steps"] = _min_steps
                _parent_id = i["parent_id"]
                self.channel_producer.basic_publish(
                    properties=pika.BasicProperties(priority=9),
                    exchange='', 
                    routing_key=os.environ['RABBITMQ_TASKQUEUE'], 
                    body="["+str(i)+"]")
        self.total_tasks = count
        count = 0
        _queue = str(self.portfolio_id) + "_" + str(_parent_id)
        self.channel_consumer_parent.queue_declare(queue=_queue)
        self.channel_consumer_parent.basic_qos(prefetch_count=int(os.environ['RABBITMQ_PREFETCHCOUNT']))
        self.channel_consumer_parent.basic_consume(queue=_queue, auto_ack=True, on_message_callback=self.callback_parent)
        self.channel_consumer_parent.start_consuming()
        self.connection2.close()

    def __init__(self):
        while True:
            self.connection1 = pika.BlockingConnection(pika.ConnectionParameters(os.environ['RABBITMQ_HOST']))
            self.channel_consumer_splittable = self.connection1.channel()
            self.channel_consumer_splittable.queue_declare(queue=os.environ['RABBITMQ_TASKQUEUE_SPLITTABLE'])
            self.channel_consumer_splittable.basic_qos(prefetch_count=int(os.environ['RABBITMQ_PREFETCHCOUNT']))
            self.channel_consumer_splittable.basic_consume(queue=os.environ['RABBITMQ_TASKQUEUE_SPLITTABLE'], auto_ack=True, on_message_callback=self.callback)
            self.channel_consumer_splittable.start_consuming()
