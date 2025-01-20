import redis


# 创建连接
def connect_redis(host='1.94.147.176', password='kjiolluy711', port=6379, db=0):
    return redis.StrictRedis(host=host, password=password, port=port, db=db, decode_responses=True)


# 字符串操作
class RedisString:
    @staticmethod
    def set_data(key, value, redis_conn=None):
        if not redis_conn: redis_conn = connect_redis()
        return redis_conn.set(key, value)

    @staticmethod
    def get_data(key, redis_conn=None):
        if not redis_conn: redis_conn = connect_redis()
        return redis_conn.get(key)

# 列表操作
class RedisList:
    @staticmethod
    def add_to_list(key, *values, redis_conn=None):
        if not redis_conn: redis_conn = connect_redis()
        return redis_conn.rpush(key, *values)

    @staticmethod
    def get_list(key, start=0, end=-1, redis_conn=None):
        if not redis_conn: redis_conn = connect_redis()
        return redis_conn.lrange(key, start, end)

# 集合操作
class RedisSet:
    @staticmethod
    def add_to_set(key, *members, redis_conn=None):
        if not redis_conn: redis_conn = connect_redis()
        return redis_conn.sadd(key, *members)

    @staticmethod
    def get_members(key, redis_conn=None):
        if not redis_conn: redis_conn = connect_redis()
        return redis_conn.smembers(key)

# 有序集合操作
class RedisSortedSet:
    @staticmethod
    def add_to_sorted_set(key, mapping, redis_conn=None):
        if not redis_conn: redis_conn = connect_redis()
        return redis_conn.zadd(key, mapping)

    @staticmethod
    def get_range_by_score(key, min_score, max_score, redis_conn=None):
        if not redis_conn: redis_conn = connect_redis()
        return redis_conn.zrangebyscore(key, min_score, max_score)

# 哈希表操作
class RedisHash:
    @staticmethod
    def set_hash_data(key, mapping, redis_conn=None):
        if not redis_conn: redis_conn = connect_redis()
        # 使用 hset 替代 hmset
        for field, value in mapping.items():
            redis_conn.hset(key, field, value)
        return True

    @staticmethod
    def get_hash_data(key, fields=None, redis_conn=None):
        if not redis_conn: redis_conn = connect_redis()
        if fields:
            return redis_conn.hmget(key, fields)
        else:
            return redis_conn.hgetall(key)

# 示例使用
if __name__ == '__main__':
    # 字符串操作示例
    RedisString.set_data('test_string', 'hello')
    print(RedisString.get_data('test_string'))

    # 列表操作示例
    RedisList.add_to_list('test_list', 'item1', 'item2')
    print(RedisList.get_list('test_list'))

    # 集合操作示例
    RedisSet.add_to_set('test_set', 'member1', 'member2')
    print(RedisSet.get_members('test_set'))

    # 有序集合操作示例
    RedisSortedSet.add_to_sorted_set('test_zset', {'member1': 1, 'member2': 2})
    print(RedisSortedSet.get_range_by_score('test_zset', 1, 2))

    # 哈希表操作示例
    RedisHash.set_hash_data('test_hash', {'field1': 'value1', 'field2': 'value2'})
    print(RedisHash.get_hash_data('test_hash'))