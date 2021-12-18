import redis
from config.config import Configuration

r = redis.Redis(host=Configuration.REDIS_HOST, port=int(Configuration.REDIS_PORT), db=0)
