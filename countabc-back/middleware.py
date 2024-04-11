import redis
from models import PyBase,RedBase,ER_RedBase,Stats
import string

import datetime,random
class RedisDB:
    def __init__(self,username,password,host,port,db):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.db = db
    
    def connect(self):
        try:
            self.r = redis.Redis(host=self.host,port=self.port,db=self.db,password=self.password,username=self.username,decode_responses=True,retry_on_timeout=True,charset="utf-8")
            print("Connected to Database")
        except Exception as e:
            print("Error connecting to Redis: ",e)
            raise e
    def setup(self):
        exists=Stats(**self.r.hgetall("stats"))
        self.r.hset("stats",mapping=exists.model_dump())
        return
    # @staticmethod
    def hit_count(self):
        # def wrapper(self,*args,**kwargs):
        stats=Stats(**self.r.hgetall("stats"))
        stats.requests+=1
        self.r.hset("stats",mapping=stats.model_dump())
            # return func(self,*args,**kwargs)
        # return wrapper

    @staticmethod
    def check_key(error_message_func):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                key = args[0] or kwargs.get("key", "shubhmittal::pplop")
                stats = Stats(**self.r.hgetall("stats"))
                self.r.hset("stats", mapping=stats.model_dump())
                if self.r.exists(key):
                    self.r.expire(key, 6 * 30 * 24 * 60 * 60)  # 6 months
                    return func(self, *args, **kwargs)
                else:
                    err_message = error_message_func()  # Call the provided error message function
                    return 404, err_message
            return wrapper
        return decorator
    
    def new_key(self,key,mappings={}):
        exisitng=self.r.exists(key)
        if not exisitng:
            self.r.hset(key,mapping=RedBase(**mappings).model_dump())
            self.r.expire(key,6*30*24*60*60)#6 months
            keys=Stats(**self.r.hgetall("stats"))
            keys.keys_created+=1
            self.r.hset("stats",mapping=keys.model_dump())
            # print("Key created")
            return 200,RedBase(**mappings).model_dump()
        else:
            print("Key already exists")

            return 409,ER_RedBase().model_dump()

    
    @check_key(error_message_func=lambda: {"old_value": None, "new_value": None})
    def set_value(self,key,value,err_message={"old_value":None,"new_value":None}):
        # pass
        curr_value=PyBase(**self.r.hgetall(key))
        # print(curr_value)
        if curr_value.enable_reset:
            self.r.hset(key,"value",value)
            stats=Stats(**self.r.hgetall("stats"))
            stats.keys_updated+=1
            self.r.hset("stats",mapping=stats.model_dump())
            return 200,{"old_value":curr_value.value,"new_value":value}
        else:
            return 403,{"old_value":curr_value.value,"new_value":curr_value.value}
    
    @check_key(error_message_func=lambda: {"value": None})
    def update_value(self,key,value=None):
        # pass
        curr_value=PyBase(**self.r.hgetall(key))
        # if curr_value.get("")
        print(value)
        if value in range(curr_value.update_lowerbound,curr_value.update_upperbound+1):
            self.r.hset(key,"value",curr_value.value+value)
            stats=Stats(**self.r.hgetall("stats"))
            stats.keys_updated+=1
            self.r.hset("stats",mapping=stats.model_dump())
            return 200,{"value":curr_value.value+value}
        else:
            return 403,{"value":curr_value.value}
    
    # @check_key
    def hit_value(self,key):
        if not self.r.exists(key):
            res=self.new_key(key)
            return 200,{"value":1}
        else:
            return self.update_value(key,value=1)
    
    @check_key(error_message_func=lambda: {"value": None})
    def get_value(self,key):
        return 200,{"value": PyBase(**self.r.hgetall(key)).value}
    
    
    @check_key(error_message_func=lambda: ER_RedBase().model_dump())
    def get_info(self,key):
        return 200,PyBase(**self.r.hgetall(key)).model_dump()
        
    def get_stats(self):
        return 200,Stats(**self.r.hgetall("stats")).model_dump()
    
    def get_namespace(self,namespace):
        keys=self.r.keys(f"{namespace}:*")
        return 200,keys


def generate_random_key():
    # Get the current date and time
    current_datetime = datetime.datetime.now()
    
    # Format the datetime as a string (you can customize the format)
    formatted_datetime = current_datetime.strftime("%Y%m%d%H%M%S")
    
    # Generate a random component (e.g., a random string of characters)
    random_component = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    
    # Combine the formatted datetime and random component to create the key
    key = f"{formatted_datetime}-{random_component}"
    return key

    
# a=RedisDB("default","shubh2003","redis-14419.c212.ap-south-1-1.ec2.cloud.redislabs.com",14419,0)
# a.connect()
# # a.setup()
# # print(a.get_value("default:shubh")) #Check 2/2
# # print(a.set_value("shubh",value=288)) #Check 3/3
# print(a.update_value("default:shubh",value=1)) #Check 3/3
# print(a.hit_value("njnj"))
# print(a.new_key("njnjnjjj",{"namespace":"shubh"}))
# print(a.get_info("mkm"))
# print(a.get_stats())
# # print(a.key_exists("test")==True)
# print(a.set_value("shubh"))