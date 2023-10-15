import os
import smartninja_redis


redis = smartninja_redis.from_url(os.environ.get('REDIS_URL'))
