import json
import requests
from faker import Faker
from datetime import datetime


fake = Faker()

# URL API
api_url = "http://localhost:8000/contacts/"

num_fake_contacts = 10

for _ in range(num_fake_contacts):

    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    phone_number = fake.phone_number()
    birth_date = fake.date_of_birth(minimum_age=18, maximum_age=65)
    additional_info = fake.text()

    birth_date_str = birth_date.isoformat()
    contact_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone_number": phone_number,
        "birth_date": birth_date_str,
        "additional_info": additional_info,
    }

    response = requests.post(api_url, json=contact_data)

    if response.status_code == 201:
        print(f"Створено контакт: {first_name} {last_name}")
    else:
        print(f"Помилка при створенні контакту: {response.status_code}")
