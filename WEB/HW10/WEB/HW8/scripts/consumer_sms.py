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
                print(f"Processing SMS for contact with ID: {contact_id}")

                fake_sms = fake.text()
                channel.basic_publish(exchange='', routing_key='sms_queue', body=json.dumps(fake_sms).encode())

                contact.sms_sent = True
                contact.save()
            except Contact.DoesNotExist:
                print(f"Contact with ID {contact_id} does not exist")
        else:
            print("Invalid SMS data format: 'contact_id' not found")
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")


# Change the queue to sms_queue
channel.basic_consume(queue="sms_queue", on_message_callback=callback, auto_ack=True)

print("Waiting for SMS messages. To exit press CTRL+C")
channel.start_consuming()
