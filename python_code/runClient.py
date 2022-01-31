import os, pika, json, threading
from datetime import datetime
from random import randrange
import splunklib.client as splunk_client
import numpy as np

class client:
    total_tasks = 0
    portfolio_id = ""
    callback_count = 0
    portfolio_result = ""
    channel_producer = ""
    channel_producer_splittable = ""
    channel_consumer = ""
    connection = ""
    start_time = ""
    to_splunk_string = ""

    def format_paths(self, _json):
        data = eval(_json)
        _num_sims = int(data["num_sims"])
        _num_steps = int(data["num_steps"])
        paths = data["paths"].replace("],", "];")
        paths = list(paths.split(";"))
        list_paths = []
        count = 0
        for k in paths:
            level1_paths = paths[count].replace("[", "").replace("]", "").replace(" ", "")
            level1_paths = list(level1_paths.split(","))
            list_paths.append(level1_paths)
            count = count + 1
        count = 0
        _exit = 0
        transpose = np.transpose(list_paths)
        temp_paths = []
        for i in range(_num_sims):
            temp_subpaths = []
            for k in range(_num_steps):
                if (temp_subpaths == []):
                    temp_subpaths = [{"sub_path_id": str(i)+","+str(k), "sub_path_value": float(transpose[i][k])}]
                else:
                    temp_subpaths.append({"sub_path_id": str(i)+","+str(k), "sub_path_value": float(transpose[i][k])})
            if (temp_paths == []):
                temp_paths = [{"path_id": i, "path_value": temp_subpaths}]
            else:
                temp_paths.append({"path_id": i, "path_value": temp_subpaths})

        return temp_paths

    def format_paths_max(self, _json):
        data = eval(_json)
        paths_max = data["paths_max"].replace("[", "").replace("]", "").replace(" ", "")
        paths_max = list(paths_max.split(","))
        count = 0
        for i in paths_max:
            if (count == 0):
                temp = [{"path_max_id": count, "value": float(paths_max[count])}]
            else:
                temp.append({"path_max_id": count, "value": float(paths_max[count])})
            count = count + 1
        return temp

    def callback(self, ch, method, properties, body):
        reporting = os.environ['REPORTING']
        if (reporting == "0"):
            if (self.callback_count <= self.total_tasks):
                data = eval(body)
                onclient_time = {"onclient_time": str(datetime.now())}
                data.update(onclient_time)
                paths_max = {"paths_max": self.format_paths_max(body)}
                data.update(paths_max)
                paths = {"paths": self.format_paths(body)}
                data.update(paths)
                if (self.callback_count == 0):
                    self.portfolio_result = str(data)
                else:
                    self.portfolio_result = self.portfolio_result + "," + str(data)
                self.callback_count = self.callback_count + 1
                if (self.callback_count == self.total_tasks):
                    _result = "[" + self.portfolio_result + "]"
                    self.to_splunk_string = _result.replace("\'", "\"")
                    #print(self.to_splunk_string)
                    end_time = datetime.now()
                    total_time = end_time - self.start_time
                    #print("RESULT: " + str(_result))
                    print("PORTFOLIO TIME: " + str(total_time))
                    _queue = str(self.portfolio_id) + "_result"
                    self.channel_consumer.queue_delete(queue=_queue)
                    self.channel_consumer.stop_consuming()
        else:
            if (reporting == "1"):
                if (self.callback_count <= self.total_tasks):
                    self.callback_count = self.callback_count + 1
                    print("TASKS RECEIVED: " + str(self.callback_count))
                    if (self.callback_count == self.total_tasks):
                        end_time = datetime.now()
                        total_time = end_time - self.start_time
                        print(body)
                        print("PORTFOLIO TIME: " + str(total_time))
                        _queue = str(self.portfolio_id) + "_result"
                        self.channel_consumer.queue_delete(queue=_queue)
                        self.channel_consumer.stop_consuming()

    def __init__(self, _file):
        ## MAIN
        
        ## Reading simulations JSON file
        form = _file
        f = open(form,)
        data = json.load(f)
        _new_portfolio_id = randrange(10000)
        for k in data:
            k["portfolio_id"] = str(_new_portfolio_id)

        print("PORTFOLIO_ID: " + str(_new_portfolio_id))
        self.start_time = datetime.now()
        print("START TIME: " + str(self.start_time))
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ['RABBITMQ_HOST']))
        self.channel_producer = self.connection.channel()
        self.channel_producer.queue_declare(queue=os.environ['RABBITMQ_TASKQUEUE'], arguments={"x-max-priority": 10})
        self.channel_producer_splittable = self.connection.channel()
        self.channel_producer_splittable.queue_declare(queue=os.environ['RABBITMQ_TASKQUEUE_SPLITTABLE'])

        print("CLIENT SPLITING...")
        for k in data:
            self.total_tasks = self.total_tasks + 1
            self.portfolio_id = k["portfolio_id"]
            submit_time = {"submit_time": str(datetime.now())}
            k.update(submit_time)
            if (int(k["num_steps"]) > int(os.environ['NUM_STEPS'])):
                self.channel_producer_splittable.basic_publish(
                    exchange='', 
                    routing_key=os.environ['RABBITMQ_TASKQUEUE_SPLITTABLE'], 
                    body="["+str(k)+"]")
            else:
                self.channel_producer.basic_publish(
                    exchange='', 
                    routing_key=os.environ['RABBITMQ_TASKQUEUE'], 
                    body="["+str(k)+"]")

        aux = datetime.now()
        send_time = aux - self.start_time
        print("SEND TIME: " + str(send_time))

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ['RABBITMQ_HOST']))
        self.channel_consumer = self.connection.channel() 
        _queue = str(self.portfolio_id) + "_result"
        self.channel_consumer.queue_declare(queue=_queue)
        self.channel_consumer.basic_qos(prefetch_count=500)
        self.channel_consumer.basic_consume(queue=_queue, auto_ack=True, on_message_callback=self.callback)
        self.channel_consumer.start_consuming()

        if (int(os.environ['REPORTING']) == 0):
            service = splunk_client.connect(host=os.environ['SPLUNK_HOST'],port=8089,username=os.environ['SPLUNK_USER'],password=os.environ['SPLUNK_PASSWORD'])
            myindex = service.indexes[os.environ['SPLUNK_INDEX']]
            print(myindex)
            mysocket = myindex.attach(sourcetype=os.environ['SPLUNK_SOURCETYPE'],host='client')
            mysocket.send(self.to_splunk_string.encode())
            mysocket.close()