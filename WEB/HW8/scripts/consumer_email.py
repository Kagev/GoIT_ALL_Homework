import pika
import json
from scripts.connect import create_connection_rabbitmq, create_connection_mongodb
from data.models import Contact
from faker import Faker

fake = Faker("uk-UA", use_weighted_distribution=True)

channel, connection = create_connection_rabbitmq()
create_connection_mongodb()  # Establish a connection to MongoDB


def callback(ch, method, properties, body):
    try:
        data = json.loads(body.decode("utf-8"))
        if "contact_id" in data:
            contact_id = data["contact_id"]
            try:
                contact = Contact.objects.get(id=contact_id)
                print(f"Processing EMAIL contact with ID: {contact_id}")

                fake_message = fake.text()  # Generate a fake message
                channel.basic_publish(exchange='', routing_key='email_queue', body=json.dumps(fake_message).encode())

                contact.message_sent = True
                contact.save()
            except Contact.DoesNotExist:
                print(f"Contact with ID {contact_id} does not exist")
        else:
            print("Invalid EMAIL data format: 'contact_id' not found")
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")



channel.basic_consume(queue="email_queue", on_message_callback=callback, auto_ack=True)

print("Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
