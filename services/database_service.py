import logging
import json
import os

from flask import jsonify
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

logging.basicConfig(level=logging.DEBUG)

from pymongo import MongoClient


# This service is for database manipulation

def add_paragraph(paragraph):
    user = "admin"
    password = os.getenv('MONGODBPASSWORD')
    client = MongoClient(
        "mongodb+srv://" + user + ":" + password + "@cluster0.xcvzv0m.mongodb.net/?retryWrites=true&w=majority",
        server_api=ServerApi('1'))
    db = client["fyp"]
    collection = db["paragraphs"]

    insert_result = collection.insert_one(paragraph)
    # get the ObjectId of the inserted document
    inserted_id = insert_result.inserted_id
    # update the document with the 1st_element field containing the ObjectId
    collection.update_one({"_id": inserted_id}, {"$set": {"parallel_sentences.0.id": str(inserted_id)}})
    # paragraph["parallel_sentences"][0]["id"] = str(inserted_id)


    # return the inserted document w/ the _id field
    logging.info(paragraph)
    return jsonify(paragraph)


def add_sentence(data):
    user = "admin"
    password = os.getenv('MONGODBPASSWORD')
    client = MongoClient(
        "mongodb+srv://" + user + ":" + password + "@cluster0.xcvzv0m.mongodb.net/?retryWrites=true&w=majority",
        server_api=ServerApi('1'))
    db = client["fyp"]
    collection = db["paragraphs"]

    # Extract the originalParagraphId & newParagraphId & sentence property from the data object
    original_paragraph_id = data['originalParagraphId']
    sentence = data['sentence']
    new_paragraph_id = data['newParagraphId']
    # Find the document where to add the new sentence
    query = {"_id": ObjectId(original_paragraph_id)}
    document = collection.find_one(query)
    logging.info(document)
    new_object = {"id": new_paragraph_id, "sentence": sentence}
    # Append the new id & sentence to the existing sentences array
    document["parallel_sentences"].append(new_object)
    # Update the document in the MongoDB collection
    response = collection.update_one(query, {"$set": {"parallel_sentences": document["parallel_sentences"]}})


def add_revealed_to_hidden(data):
    user = "admin"
    password = os.getenv('MONGODBPASSWORD')
    client = MongoClient(
        "mongodb+srv://" + user + ":" + password + "@cluster0.xcvzv0m.mongodb.net/?retryWrites=true&w=majority",
        server_api=ServerApi('1'))
    db = client["fyp"]
    collection = db["paragraphs"]

    # Extract the originalParagraphId & chosenIndex property from the data object
    original_paragraph_id = data['originalParagraphId']
    chosen_index = data['chosenIndex']
    insert_revealed = data['insertRevealed']

    # Find the document where to add the new revealed
    query = {"_id": ObjectId(original_paragraph_id)}
    document = collection.find_one(query)

    # Remove the chosen item from the 'revealed' array
    removed_item = document['revealed'].pop(chosen_index)

    # Get the index where the new items will be inserted
    index_to_insert = chosen_index

    # Modify the new items to set their start indices
    # for item in insert_revealed:
    #     item['index_interval_start'] += index_to_insert
    # Insert the new items into the 'revealed' array
    for item in reversed(insert_revealed):
        matching_item = next((x for x in document['revealed'] if x['index_interval_start'] == item['index_interval_start']), None)
        if matching_item:
            matching_item['index_interval_end'] += 1
        else:
            document['revealed'].insert(index_to_insert, item)

    # check for duplicate and merge them
    # new_revealed = []
    # for item in document['revealed']:
    #     if item not in new_revealed:
    #         new_revealed.append(item)
    #     else:
    #         index = new_revealed.index(item)
    #         new_revealed[index]['count'] += 1
    # document['revealed'] = new_revealed
    # Update the document in the MongoDB collection
    response = collection.replace_one(query, document)
    return response


def add_work_id_to_user(data):
    user = "admin"
    password = os.getenv('MONGODBPASSWORD')
    client = MongoClient(
        "mongodb+srv://" + user + ":" + password + "@cluster0.xcvzv0m.mongodb.net/?retryWrites=true&w=majority",
        server_api=ServerApi('1'))
    db = client["fyp"]
    collection = db["users"]

    # Extract the workId & userName  property from the data object
    work_id = data['workId']
    user_name = data['userName']
    # Find the document where to add the new sentence
    query = {"username": user_name}
    document = collection.find_one(query)
    logging.info(document)
    # Append the work_id to the existing works array
    if "works" in document:
        document["works"].append(work_id)
    else:
        document["works"] = [work_id]
    # Update the document in the MongoDB collection
    response = collection.update_one(query, {"$set": {"works": document["works"]}})



# login signup
def signup(username, email, password, isSigningUp):
    # connect to the db
    user = "admin"
    dbpassword = os.getenv('MONGODBPASSWORD')
    client = MongoClient(
        "mongodb+srv://" + user + ":" + dbpassword + "@cluster0.xcvzv0m.mongodb.net/?retryWrites=true&w=majority",
        server_api=ServerApi('1'))
    db = client["fyp"]
    collection = db["users"]

    if isSigningUp:
        # Perform sign-up
        collection.insert_one({'username': username, 'email': email, 'password': password})
        message = 'Successfully signed up'
    else:
        # Perform sign-in
        return collection.find_one({'username': username, 'email': email, 'password': password})
    return jsonify({'message': message})


# Users database related


# def add_user(data):
#     user = "admin"
#     password = os.getenv('MONGODBPASSWORD')
#     client = MongoClient(
#         "mongodb+srv://" + user + ":" + password + "@cluster0.xcvzv0m.mongodb.net/?retryWrites=true&w=majority",
#         server_api=ServerApi('1'))
#     db = client["fyp"]
#     collection = db["users"]
#
#     # construct user object (new dictionary of user) if data dictionary contains both password and username keys
#     # logging.info(data)
#     if data["password"] and data["username"]:
#         user = {
#             "password": data["password"],
#             "username": data["username"]
#         }
#
#         # Insert the object
#         logging.info("Inserting user: ")
#         logging.info(user)
#         # inserts the user object into the users collection in the database
#         response = collection.insert_one(user)
#         logging.info(response)
#         return "Created user."
#     else:
#         return "Password or username missing."


def get_user_access(username):
    # connect to the db
    user = "admin"
    password = os.getenv('MONGODBPASSWORD')
    client = MongoClient(
        "mongodb+srv://" + user + ":" + password + "@cluster0.xcvzv0m.mongodb.net/?retryWrites=true&w=majority",
        server_api=ServerApi('1'))
    db = client["fyp"]
    collection = db["users"]

    # find currentUser by username
    currentUser = collection.find_one({"username": username})

    # check if currentUser exist
    if currentUser:
        # get access restrictions & return
        access = user.get("access")
        return jsonify({"access": access})
    else:
        return "user not found."
