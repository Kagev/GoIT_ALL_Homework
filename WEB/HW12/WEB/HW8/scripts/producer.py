import json
from colorama import init, Fore
from pika import BlockingConnection, ConnectionParameters
from redis_lru import RedisLRU
from faker import Faker
from data.models import Contact
from scripts.connect import create_connection_mongodb, create_connection_redis, create_connection_rabbitmq

fake = Faker("uk-UA", utf=8)

redis_client = create_connection_redis()
cache = RedisLRU(redis_client)

connection = create_connection_mongodb()
channel, _ = create_connection_rabbitmq()

init(autoreset=True)


def rabbit_fake_data():
    return {
        "fullname": fake.name(),
        "born_date": fake.date_of_birth(),
        "email": fake.email(),
        "phone_number": fake.phone_number(),
        "prefer_sms": fake.random_element([True, False])
    }


def generation_data():
    num_contacts = 20  # Количество фейковых контактов

    for _ in range(num_contacts):
        contact_data = rabbit_fake_data()
        contact = Contact(**contact_data)
        contact.save()

        message = {"contact_id": str(contact.id)}

        if contact.prefer_sms:
            channel.queue_declare(queue="sms_queue")
            queue_name = "sms_queue"
        else:
            channel.queue_declare(queue="email_queue")
            queue_name = "email_queue"

        channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(message))
        print(f"Sent contact with ID: {contact.id} to {queue_name}")


if __name__ == "__main__":
    generation_data()
