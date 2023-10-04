import json
import pathlib

from data.models import Author, Quote
from connect import create_connection, check_database_connection

connection = create_connection()

file_json = pathlib.Path(__file__).parent.parent.joinpath("json")


def author_file_json():
    with open(f"{file_json}/authors.json", "r") as authors_file:
        authors_data = json.load(authors_file)
        for author_data in authors_data:
            Author(**author_data).save()


def quotes_file_json():
    with open(f"{file_json}/quotes.json", "r") as quotes_file:
        quotes_data = json.load(quotes_file)
        for quote_data in quotes_data:
            author_name = quote_data["author"]
            author = Author.objects(fullname=author_name).first()
            if author:
                quote_data["author"] = author
                Quote(**quote_data).save()


if __name__ == "__main__":
    author_file_json()
    quotes_file_json()
