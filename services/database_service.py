import logging
import json

from pymongo.server_api import ServerApi

logging.basicConfig(level=logging.DEBUG)

from pymongo import MongoClient


# This service is for database manipulation

def add_paragraph(paragraph):
    # Read file contents
    with open('paragraphs.json', "r+") as file:
        data = json.load(file)

        # Update json object
        data.append(paragraph)

        file.seek(0)

        # Write to file
        json.dump(data, file)

    """
    # Connect to db
    user = "admin"
    password = "DERceoY4DwgQQ9CT"
    client = MongoClient(
        "mongodb+srv://" + user + ":" + password + "@cluster0.xcvzv0m.mongodb.net/?retryWrites=true&w=majority",
        server_api=ServerApi('1'))
    logging.debug(client)

    # Get db
    db = client["fyp"]
    logging.debug(db)

    # Get collection
    collection = db["paragraphs"]
    logging.debug(collection)

    # Construct data object
    paragraph = {
        "paragraph": "Through decades that ran like rivers…",
        "id": "flG47F77IQ",
        "creator_id": "vjakukfe",
        "revealed": [
            {
                "index_intervall": "0:20",
                "revealed_score": 1,
            },
            {
                "index_intervall": "20:360",
                "revealed_score": 0,
            }
        ]
    }

    # Insert the object
    response = collection.insert_one(paragraph)
    logging.info(response)
    """
