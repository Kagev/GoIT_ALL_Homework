# Connect to MongoDB
from datetime import datetime
import pymongo

mongo_client = pymongo.MongoClient('mongodb+srv://kagev:kVIbY5iArpTmbFVi@cluster0.8qdpzku.mongodb.net/')

# Select MongoDB database and collections
mongo_db = mongo_client['homework8']
mongo_authors = mongo_db['author']
mongo_quotes = mongo_db['quote']

# Loop through MongoDB data and transfer to PostgreSQL
for mongo_author in mongo_authors.find():
    born_date_str = mongo_author.get('born_date', None)
    born_date = datetime.strptime(born_date_str, "%B %d, %Y") if born_date_str else None

    fullname=mongo_author['fullname']
#     born_date=born_date
#     born_location=mongo_author.get('born_location', None)
#     description=mongo_author.get('description', None)
#
#     print(f"fullname: {fullname}")
#     print(f"born_date: {born_date}")
#     print(f"born_location: {born_location}")


    for mongo_quote in mongo_quotes.find():
        # {'author.$id': mongo_author['_id']}
        tags = mongo_quote['tags']
        mongo_authors = mongo_db['author']
        author = mongo_author['fullname']
        quote = mongo_quote['quote']

        print(f"Tags: {tags}")
        print(f"Author: {author}")
        print(f"Quote: {quote}")
            # Quote.objects.create(
            #     tags=mongo_quote['tags`'],
            #     author=mongo_author['fullname'],
            #     quote=mongo_quote['quote']
            # )

