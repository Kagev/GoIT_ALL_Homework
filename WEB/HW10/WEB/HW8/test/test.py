import argparse
import json
import redis
from colorama import init, Fore
from connect import create_connection
from data.models import Author, Quote
from redis_lru import RedisLRU

init(autoreset=True)

redis_client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(redis_client)

connection = create_connection()
quotes_collection = Quote.objects


@cache
def search_quotes(query):
    cached_quotes = redis_client.get(query)

    if cached_quotes:
        return json.loads(cached_quotes)

    if query.startswith("name:"):
        author_name = query[5:]
        quotes = list(quotes_collection.filter(author__icontains=author_name))
    elif query.startswith("tag:"):
        tag = query[4:]
        quotes = list(quotes_collection.filter(tags__in=[tag]))
    elif query.startswith("tags:"):
        tags = query[5:].split(',')
        quotes = list(quotes_collection.filter(tags__all=tags))
    else:
        quotes = []

    serializable_quotes = []
    for quote in quotes:
        serializable_quote = {
            "author": quote.author,
            "text": quote.text,
            "tags": quote.tags,
        }
        serializable_quotes.append(serializable_quote)

    redis_client.set(query, json.dumps(serializable_quotes))
    return serializable_quotes



if __name__ == "__main__":
    while True:

        parser = argparse.ArgumentParser(description="Search for quotes by name, tag, or tags.")
        parser.add_argument("name", "-n", "--name", help="Search quotes by author's name")
        parser.add_argument("tag", "-t", "--tag", help="Search quotes by a single tag")
        parser.add_argument("tags", "-ts", "--tags", nargs="+", help="Search quotes by multiple tags")

        print("____" * 10)
        print("If you want search 'AUTHOR' need to enter command" + Fore.YELLOW + "'-n' or '--name' or 'name'")
        print("If you want search 'TAG' need to enter command" + Fore.YELLOW + "'-t' or '--tag' or 'tag'")
        print("If you want search 'TAGS' need to enter command" + Fore.YELLOW + "'-ts' or '--tags' or 'tags'. Example: -ts live, life")
        print("If you want QUIT enter command" + Fore.YELLOW + "'EXIT'")
        print("____" * 10)

        input_user = input(">>> Yor search command: ")

        args = parser.parse_args(input_user.split())

        if not input_user:
            print("Please provide valid input.")
        elif input_user.lower() == 'exit':
            break
        elif args.name:
            quotes = search_quotes(f"name:{args.name}")
            print(quotes)
        elif args.tag:
            cleaned_tag = [tag.strip().replace(",", "").replace(" ", "").lower() for tag in args.tag if tag.strip()]
            tags_query = "tag:" + cleaned_tag[0]
            quotes = search_quotes(tags_query)
            print(quotes)
        elif args.tags:
            cleaned_tags = [tag.strip().replace(",", "").replace(" ", "").lower() for tag in args.tags if tag.strip()]
            cleaned_tags = [tag.strip().replace(",", "").replace(" ", "").lower() for tag in args.tags if tag.strip()]
            tags_query = "tags:" + ",".join(cleaned_tags)
            quotes = search_quotes(tags_query)
            print(quotes)
