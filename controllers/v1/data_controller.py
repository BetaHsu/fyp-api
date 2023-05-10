import logging
import json
import os

from flask import make_response, request, jsonify, render_template
from pymongo.server_api import ServerApi

logging.basicConfig(level=logging.DEBUG)

from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps

from app import app
from services import database_service


def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


@app.route("/api/test", methods=["GET", "OPTIONS"])
def hello_world():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    elif request.method == "GET":
        print(os.getenv('MONGODBPASSWORD'))
        response = make_response("<p>API works.</p>")
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response
    else:
        return make_response("Unknown method.")


@app.route("/api/v1/get-paragraph/<paragraph_id>", methods=["GET", "OPTIONS"])
def get_paragraph(paragraph_id):
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    elif request.method == "GET":
        user = "admin"
        password = os.getenv('MONGODBPASSWORD')
        client = MongoClient(
            "mongodb+srv://" + user + ":" + password + "@cluster0.xcvzv0m.mongodb.net/?retryWrites=true&w=majority",
            server_api=ServerApi('1'))
        db = client["fyp"]
        collection = db["paragraphs"]

        # query = {"id": paragraph_id}
        query = {"_id": ObjectId(paragraph_id)}
        paragraph = collection.find_one(query)
        logging.info(paragraph)
        if paragraph:
            paragraph['_id'] = str(paragraph['_id'])
            response = make_response(jsonify(paragraph), 200)
        else:
            response = make_response("Paragraph not found", 404)
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response
    else:
        return make_response("Unknown method.")


@app.route("/api/v1/get-all-paragraph-id", methods=["GET", "OPTIONS"])
def get_all_paragraph_id():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    elif request.method == "GET":
        user = "admin"
        password = os.getenv('MONGODBPASSWORD')
        client = MongoClient(
            "mongodb+srv://" + user + ":" + password + "@cluster0.xcvzv0m.mongodb.net/?retryWrites=true&w=majority",
            server_api=ServerApi('1'))
        db = client["fyp"]
        collection = db["paragraphs"]
        # paragraphs = list(collection.find({}, {"_id": 1}))

        if collection is not None: # compare collection with None instead of using it as a boolean
            # find all documents and only retrieve "_id" & "title" fields,
            # convert pymongo cursor object to list of dictionaries
            paragraphs = list(collection.find({}, {"_id": 1, "title": 1, "parallel_sentences.id": 1, "reveal_score_to_public": 1}))
            # paragraph_ids = [str(paragraph["_id"]) for paragraph in paragraphs]
            # logging.info(paragraphs)
            response = make_response(dumps(paragraphs), 200)
        else:
            response = make_response("Paragraph not found", 404)

        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response
    else:
        return make_response("Unknown method.")


@app.route("/api/v1/get-user-works/<username>", methods=["GET", "OPTIONS"])
def get_user_works(username):
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    elif request.method == "GET":
        user = "admin"
        password = os.getenv('MONGODBPASSWORD')
        client = MongoClient(
            "mongodb+srv://" + user + ":" + password + "@cluster0.xcvzv0m.mongodb.net/?retryWrites=true&w=majority",
            server_api=ServerApi('1'))
        db = client["fyp"]
        collection = db["users"]

        current_user = collection.find_one({"username": username})
        if current_user:
            works = current_user.get("works", [])
            response = make_response(jsonify(works), 200)
        else:
            response = make_response("User not found", 404)

        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response
    else:
        return make_response("Unknown method.")


@app.route("/api/v1/post-paragraph", methods=["POST", "OPTIONS"])
def post_paragraphs():
    # logging.info("call post paragraph")
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    elif request.method == "POST":
        # logging.info("post_paragraph work" + str(data))
        data = request.get_json()
        response = make_response(database_service.add_paragraph(data))
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response
    else:
        return make_response("Unknown method.")


@app.route("/api/v1/post-sentence-to-parallel", methods=["POST", "OPTIONS"])
def post_sentence_to_parallel():
    data = request.get_json(force=True)
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    elif request.method == "POST":
        database_service.add_sentence(data)
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response
    else:
        return make_response("Unknown method.")


# @app.route("/api/v1/post-revealed-to-change", methods=["POST", "OPTIONS"])
# def post_revealed_to_change():
#     data = request.get_json(force=True)
#     if request.method == "OPTIONS":
#         return _build_cors_preflight_response()
#     elif request.method == "POST":
#         updated_document = database_service.add_revealed_to_change(data)
#         response_data = {
#             'updated_revealed_array': updated_document["revealed"]
#         }
#         response = jsonify(response_data)
#         # response = make_response()
#         response.headers.add("Access-Control-Allow-Origin", "*")
#         response.headers.add("Access-Control-Allow-Headers", "*")
#         response.headers.add("Access-Control-Allow-Methods", "*")
#         return response
#     else:
#         return make_response("Unknown method.")


@app.route("/api/v1/post-revealed-object-to-replace", methods=["POST", "OPTIONS"])
def post_revealed_object_to_replace():
    data = request.get_json(force=True)
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    elif request.method == "POST":
        updated_document = database_service.replace_revealed_object(data)
        response_data = {
            'updated_revealed_array': updated_document["revealed"]
        }
        response = jsonify(response_data)
        # response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response
    else:
        return make_response("Unknown method.")


# @app.route("/api/v1/post-hidden-to-change", methods=["POST", "OPTIONS"])
# def post_hidden_to_change():
#     data = request.get_json(force=True)
#     if request.method == "OPTIONS":
#         return _build_cors_preflight_response()
#     elif request.method == "POST":
#         updated_document = database_service.add_hidden_to_change(data)
#         response_data = {
#             'updated_revealed_array': updated_document["revealed"]
#         }
#         response = jsonify(response_data)
#         # response = make_response()
#         response.headers.add("Access-Control-Allow-Origin", "*")
#         response.headers.add("Access-Control-Allow-Headers", "*")
#         response.headers.add("Access-Control-Allow-Methods", "*")
#         return response
#     else:
#         return make_response("Unknown method.")


@app.route("/api/v1/post-new-score", methods=["POST", "OPTIONS"])
def post_new_score():
    data = request.get_json(force=True)
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    elif request.method == "POST":
        database_service.update_score(data)
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response
    else:
        return make_response("Unknown method.")





@app.route("/api/v1/post-work-id-to-user", methods=["POST", "OPTIONS"])
def post_work_id_to_user():
    data = request.get_json(force=True)
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    elif request.method == "POST":
        database_service.add_work_id_to_user(data)
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response
    else:
        return make_response("Unknown method.")


# login signup
@app.route("/api/v1/signup", methods=["POST", "OPTIONS"])
def signup():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    elif request.method == 'POST':
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        isSigningUp = request.json['isSigningUp']
        response = database_service.signup(username, email, password, isSigningUp)

        if isSigningUp:
            # Perform sign-up, 201 "Created"
            if response['message'] == 'Successfully signed up':
                return jsonify({'message': 'Successfully signed up', 'username_message': '', 'email_message': ''}), 201
            else:
                return jsonify({'message': response['message'], 'username_message': response['username_message'], 'email_message': response['email_message']}), 409
        else:
            # Perform sign-in, 200 "OK", 401 "Unauthorized"
            if 'message' in response:
                return jsonify({'message': response['message'], 'username_message': response['username_message'], 'email_message': response['email_message']}), 409
            else:
                return jsonify({'userid': str(response['_id']), 'username': str(response['username'])}), 200
    return render_template('signup.html')


@app.route("/api/v1/get-user-access/<username>", methods=["GET", "OPTIONS"])
def get_user_access():
    username = request.get_json()
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    elif request.method == "POST":
        response = make_response(database_service.get_user_access(username))
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response
    else:
        return make_response("Unknown method.")
    return get_users()

# change reveal score
