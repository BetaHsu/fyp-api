import logging
import json
import os
import datetime

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


def add_revealed_to_change(data):
    user = "admin"
    password = os.getenv('MONGODBPASSWORD')
    client = MongoClient(
        "mongodb+srv://" + user + ":" + password + "@cluster0.xcvzv0m.mongodb.net/?retryWrites=true&w=majority",
        server_api=ServerApi('1'))
    db = client["fyp"]
    collection = db["paragraphs"]

    # Extract the originalParagraphId & chosenIndex property from the data object
    original_paragraph_id = data['originalParagraphId']
    selected_line_index = data['selectedLineIndex']
    line_array_copy = data['lineArrayCopy']

    # Find the document where to add the new revealed
    query = {"_id": ObjectId(original_paragraph_id)}
    document = collection.find_one(query)
    document['revealed'][selected_line_index] = line_array_copy
    collection.replace_one(query, document)
    collection.update_one(query, {"$set": {"lastUpdate": datetime.datetime.utcnow()}})
    return document


def add_hidden_to_change(data):
    user = "admin"
    password = os.getenv('MONGODBPASSWORD')
    client = MongoClient(
        "mongodb+srv://" + user + ":" + password + "@cluster0.xcvzv0m.mongodb.net/?retryWrites=true&w=majority",
        server_api=ServerApi('1'))
    db = client["fyp"]
    collection = db["paragraphs"]

    # Extract the originalParagraphId & chosenIndex property from the data object
    original_paragraph_id = data['originalParagraphId']
    new_revealed_object = data['newRevealedObject']

    # Find the document where to add the new revealed
    query = {"_id": ObjectId(original_paragraph_id)}
    document = collection.find_one(query)
    document['revealed'] = new_revealed_object
    collection.replace_one(query, document)
    collection.update_one(query, {"$set": {"lastUpdate": datetime.datetime.utcnow()}})
    return document


def update_score(data):
    user = "admin"
    password = os.getenv('MONGODBPASSWORD')
    client = MongoClient(
        "mongodb+srv://" + user + ":" + password + "@cluster0.xcvzv0m.mongodb.net/?retryWrites=true&w=majority",
        server_api=ServerApi('1'))
    db = client["fyp"]
    collection = db["paragraphs"]

    # Extract the originalParagraphId & newParagraphId & sentence property from the data object
    original_paragraph_id = data['originalParagraphId']
    new_reveal_score_to_public = data['newRevealScoreToPublic']
    # Find the document where to add the new sentence
    query = {"_id": ObjectId(original_paragraph_id)}
    # document = collection.find_one(query)
    response = collection.update_one(query, {"$set": {"reveal_score_to_public": new_reveal_score_to_public}})


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
        username_exist = collection.find_one({'username': username})
        email_exist = collection.find_one({'email': email})
        if username_exist and email_exist:
            response = {'message': 'Username and Email already exist', 'username_message': 'Username already exist', 'email_message': 'Email already exist'}
        elif username_exist:
            response = {'message': 'Username already exist', 'username_message': 'Username already exist', 'email_message': ''}
        elif email_exist:
            response = {'message': 'Email already exist', 'username_message': '', 'email_message': 'Email already exist'}
        # document = collection.find_one({'username': username, 'email': email, 'password': password})
        else:
            collection.insert_one({'username': username, 'email': email, 'password': password})
            response = {'message': 'Successfully signed up', 'username_message': '', 'email_message': ''}
    else:
        # Perform sign-in
        user = collection.find_one({'email': email, 'password': password})
        if user:
            response = user
        else:
            response = {'message': 'Incorrect email or password', 'username_message': '', 'email_message': ''}
    return response


# def get_user_access(username):
#     # connect to the db
#     user = "admin"
#     password = os.getenv('MONGODBPASSWORD')
#     client = MongoClient(
#         "mongodb+srv://" + user + ":" + password + "@cluster0.xcvzv0m.mongodb.net/?retryWrites=true&w=majority",
#         server_api=ServerApi('1'))
#     db = client["fyp"]
#     collection = db["users"]
#
#     # find currentUser by username
#     currentUser = collection.find_one({"username": username})
#
#     # check if currentUser exist
#     if currentUser:
#         # get access restrictions & return
#         access = user.get("access")
#         return jsonify({"access": access})
#     else:
#         return "user not found."
