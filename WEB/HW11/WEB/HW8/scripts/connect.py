import configparser, redis, pathlib, pika, time
from colorama import init, Fore
from mongoengine import connect
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from redis_lru import RedisLRU

init(autoreset=True)

file_config = pathlib.Path(__file__).parent.parent.joinpath("config.ini")
config = configparser.ConfigParser()
config.read(file_config)

username = config.get("mongodb", "username")
password = config.get("mongodb", "password")
database = config.get("mongodb", "database")
uri = config.get("mongodb", "uri")

redis_host = config.get("redis", "redis.host")
redis_port = config.get("redis", "redis_port")

rabbitmq_host = config.get("rabbitmq", "rabbitmq_host")
rabbitmq_port = config.get("rabbitmq", "rabbitmq_port")
rabbitmq_username = config.get("rabbitmq", "rabbitmq_username")
rabbitmq_password = config.get("rabbitmq", "rabbitmq_password")


def create_connection_mongodb():
    url = f"mongodb+srv://{username}:{password}@{uri}/{database}"
    conn = connect(host=url, alias='default')
    return conn


def create_connection_redis():
    redis_client = redis.StrictRedis(host="localhost", port=6379, password=None)
    cache = RedisLRU(redis_client)
    return cache


def create_connection_rabbitmq():
    connection_params = pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port,
                                                  credentials=pika.PlainCredentials(username=rabbitmq_username,
                                                                                    password=rabbitmq_password))
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    return channel, connection


def check_mongodb_connection():
    try:
        uri_with_auth = f"mongodb+srv://{username}:{password}@{uri}/{database}"
        client = MongoClient(uri_with_auth, server_api=ServerApi('1'))

        print(Fore.YELLOW + f'Connection to mongodb+srv://{username}:*******@{uri}/{database}')

        if client.admin.command('ping'):
            print(Fore.GREEN + "Connected to MongoDB successful!")
        else:
            print(Fore.RED + "Connection failed")
    except Exception as e:
        print(Fore.RED + "Connection error:", e)


def check_redis_connection(redis_host, redis_port):
    try:
        redis_client = redis.StrictRedis(host=redis_host, port=redis_port)
        redis_client.ping()
        if redis_client.ping():
            print(Fore.GREEN + "Connected to Redis successful!")
            return True
        else:
            print(Fore.RED + "Connected to Redis, but ping failed")
            return False
    except redis.ConnectionError:
        print(Fore.RED + "Connection to Redis failed")
        return False


def check_rabbitmq_connection(rabbitmq_host, rabbitmq_port, rabbitmq_username, rabbitmq_password):
    try:
        credentials = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
        parameters = pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials)

        connection = pika.BlockingConnection(parameters)
        connection.close()

        print(Fore.GREEN + "Connected to RabbitMQ!")
        return True
    except pika.exceptions.AMQPConnectionError:
        print(Fore.RED + "Connection to RabbitMQ failed")
        return False


if __name__ == "__main__":
    create_connection_mongodb()
    create_connection_redis()
    rabbitmq_channel, rabbitmq_connection = create_connection_rabbitmq()

    check_mongodb_connection()
    check_rabbitmq_connection(rabbitmq_host, rabbitmq_port, rabbitmq_username, rabbitmq_password)
    check_redis_connection(redis_host, redis_port)
