import json
import random

import requests
from faker import Faker
from datetime import datetime, date, timedelta

fake = Faker()

# URL API
api_url = "http://localhost:8000/contacts/create"

current_date = date.today()

start_date = current_date - timedelta(days=10)
end_date = current_date + timedelta(days=10)

num_fake_contacts = 10

access_token = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJib2Jkcm9wQHNpdGUuY29tIiwiZXhwIjoxNjk1NTU5MzkwLCJzY29wZSI6InJlZnJlc2hfdG9rZW4ifQ.qMRBm-BicqNXdcG4667dERUz6EZrOSte2u6cin_-KAA")

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

for _ in range(num_fake_contacts):

    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    phone_number = fake.phone_number()
    birth_date = fake.date_of_birth(minimum_age=18, maximum_age=65)
    birth_date = current_date + timedelta(days=random.randint(-10, 10))
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

    # Отправка POST-запроса для создания контакта
    response = requests.post(api_url, json=contact_data, headers=headers)

    if response.status_code == 201:
        print(f"Создан контакт: {first_name} {last_name}")
    else:
        print(f"Ошибка при создании контакта: {response.status_code}")
        print(response.text)
