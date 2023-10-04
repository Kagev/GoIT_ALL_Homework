FROM ubuntu:latest
LABEL authors="kagev"


# Встановлюємо залежності за допомогою Poetry
RUN pip install poetry
COPY pyproject.toml poetry.lock /app/
WORKDIR /app
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
#RUN pip install --no-cache-dir -r /app/requirements.txt
# Копіюємо файли додатку в контейнер
COPY . /app

# Встановлюємо рабочий каталог
WORKDIR /app

# Запускаємо FastAPI-застосунок через Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
