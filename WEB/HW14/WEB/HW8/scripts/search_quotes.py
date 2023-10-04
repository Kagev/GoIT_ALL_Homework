import redis
from colorama import init, Fore
from redis_lru import RedisLRU
from data.models import Author, Quote
from scripts.connect import create_connection_mongodb, create_connection_redis

redis_client = create_connection_redis()
cache = RedisLRU(redis_client)

connection = create_connection_mongodb()
quotes_collection = Quote.objects

init(autoreset=True)


def search_quotes_by_author_name(author_name):
    author = Author.objects(fullname__icontains=author_name).first()
    if author:
        quotes = Quote.objects(author=author)
        result = '\n'.join(quote.quote for quote in quotes)
        print(result)
    else:
        print("Author not found")


def search_quotes_by_tag(tag):
    quotes = Quote.objects(tags=tag)
    result = '\n'.join(quote.quote for quote in quotes)
    print(result)


def search_quotes_by_tags(tags):
    quotes = Quote.objects(tags__in=tags)
    result = '\n'.join(quote.quote for quote in quotes)
    print(result)


if __name__ == "__main__":
    create_connection_mongodb()
    create_connection_redis()

    while True:
        command = input(">>> Your search command: ")
        if not command:
            print("Please provide valid input.")
        elif command.lower() == 'exit':
            print(Fore.YELLOW + "Goodluck")
            break
        elif command.startswith('name:'):
            author_name = command.split('name:')[1].strip()
            search_quotes_by_author_name(author_name)
        elif command.startswith('tag:'):
            tag = command.split('tag:')[1].strip()
            search_quotes_by_tag(tag)
        elif command.startswith('tags:'):
            tags = command.split('tags:')[1].strip().split(',')
            search_quotes_by_tags(tags)
