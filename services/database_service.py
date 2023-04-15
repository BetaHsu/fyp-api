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

    return collection.insert_one(paragraph)


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
