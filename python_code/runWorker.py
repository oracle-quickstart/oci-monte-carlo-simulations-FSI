import os, json, pika
import numpy as np
from datetime import datetime

class splitter:
    channel_consumer = ""
    channel_producer = ""
    connection = ""

    def geo_paths(self, S, T, r, q, sigma, steps, N):
        """
        Inputs
        #S = Current stock Price
        #K = Strike Price
        #T = Time to maturity 1 year = 1, 1 months = 1/12
        #r = risk free interest rate
        #q = dividend yield
        # sigma = volatility 
        
        Output
        # [steps,N] Matrix of asset paths 
        """
        dt = T/steps
        #S_{T} = ln(S_{0})+\int_{0}^T(\mu-\frac{\sigma^2}{2})dt+\int_{0}^T \sigma dW(t)
        ST = np.log(S) +  np.cumsum(((r - q - sigma**2/2)*dt +\
                                sigma*np.sqrt(dt) * \
                                np.random.normal(size=(steps,N))),axis=0)
        return np.exp(ST)

    def callback(self, ch, method, properties, body):
        data = eval(body)
        for i in data:
            _num_sims = int(i["num_sims"])
            _num_steps = int(i["num_steps"])
            _level = int(i["level"])
            _underlying = float(i["underlying"])
            _strike = float(i["strike"])
            _riskfreerate = float(i["riskfreerate"])
            _volatility = i["volatility"]
            _maturity = i["maturity"]
            _dividendrate = float(i["dividendrate"])
            _portfolio_id = int(i["portfolio_id"])
            _parent_id = int(i["parent_id"])
            _start_time = datetime.now()
            _paths = self.geo_paths(_underlying, _maturity, _riskfreerate, _dividendrate, _volatility, _num_steps, _num_sims)
            payoffs = np.maximum(_paths[-1]-_strike, 0)
            if (_level == 0):
                _option_price = np.mean(payoffs)*np.exp(-_riskfreerate*_maturity) #discounting back to present value
                _max=np.max(_paths,axis=0)
                _max = _max.tolist()
            else:
                _option_price = 0
                _max=[]
            _end_time = datetime.now()
            _exec_time = _end_time - _start_time
            result = {}
            portfolio_id = {"portfolio_id": str(i["portfolio_id"])}
            parent_id = {"parent_id": str(i["parent_id"])}
            child_id = {"child_id": str(i["child_id"])}
            level = {"level": str(i["level"])}
            num_sims = {"num_sims": str(_num_sims)}
            num_steps = {"num_steps": str(_num_steps)}
            underlying = {"underlying": str(_underlying)}
            strike = {"strike": str(_strike)}
            riskfreerate = {"riskfreerate": str(_riskfreerate)}
            volatility = {"volatility": str(_volatility)}
            maturity = {"maturity": str(_maturity)}
            submit_time = {"submit_time": str(i["submit_time"])}
            dividendrate = {"dividendrate": str(_dividendrate)}
            myhost = os.uname()[1]
            worker = {"worker": str(myhost)}
            exec_time = {"exec_time": str(_exec_time)}
            start_time = {"start_time": str(_start_time)}
            option_price = {"option_price": str(_option_price)}
            paths = {"paths": str(_paths.tolist())}
            paths_max = {"paths_max": str(_max)}

            result.update(portfolio_id)
            result.update(parent_id)
            result.update(child_id)
            result.update(level)
            result.update(num_sims)
            result.update(num_steps)
            result.update(underlying)
            result.update(strike)
            result.update(riskfreerate)
            result.update(volatility)
            result.update(maturity)
            result.update(dividendrate)
            result.update(option_price)
            result.update(paths_max)
            result.update(paths)
            result.update(worker)
            result.update(exec_time)
            result.update(submit_time)
            result.update(start_time)
            if (str(i["level"]) == "0"):
                _queue = str(i["portfolio_id"]) + "_result"
                _end_time = datetime.now()
                end_time = {"end_time": str(_end_time)}
                result.update(end_time)
                self.channel_producer.queue_declare(queue=_queue)
                self.channel_producer.basic_publish(exchange='', routing_key=_queue, body=json.dumps(result))
            else:
                if (str(_level) == "2"):
                    _queue = str(_portfolio_id) + "_" + str(_parent_id)
                    self.channel_producer.queue_declare(queue=_queue)
                    self.channel_producer.basic_publish(exchange='', routing_key=_queue, body=json.dumps(result))

    def __init__(self):
        while True:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ['RABBITMQ_HOST']))
            self.channel_consumer = self.connection.channel()
            self.channel_producer = self.connection.channel()
            self.channel_consumer.queue_declare(queue=os.environ['RABBITMQ_TASKQUEUE'], arguments={"x-max-priority": 10})
            self.channel_consumer.basic_qos(prefetch_count=int(os.environ['RABBITMQ_PREFETCHCOUNT']))
            self.channel_consumer.basic_consume(queue=os.environ['RABBITMQ_TASKQUEUE'], auto_ack=True, on_message_callback=self.callback)
            self.channel_consumer.start_consuming()
