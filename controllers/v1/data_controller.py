import logging
import os

from flask import make_response, request

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


@app.route("/api/v1/get-paragraph", methods=["GET", "OPTIONS"])
def get_paragraph():
    paragraph = {
        "title": "A long journey from bush to concrete",
        "title_interval_start": 440,
        "title_interval_end": 478,
        "paragraph": "Through decades that ran like rivers, <br>endless rivers of endless woes. <br>Through pick and shovel sjambok and jail. <br>O such a long long journey! <br>When the motor-car came, <br>the sledge and the ox-cart began to die. <br>But for a while the bicycle made in Britain, <br>was the dream of every village boy. <br>With the arrival of the bus, <br>the city was brought into the village, <br>and we began to yearn for the place behind the horizons. <br>Such a long travail it was. <br>A long journey from bush to concrete. ",
        "id": "flG47F77IQ",
        "creator_id": "vjakukfee",
        "parallel_sentences": [
            "A long journey from bush to concrete"
        ],
        "revealed": [
            {
                "index_interval_start": 0,
                "index_interval_end": 440,
                "revealed_score": 0,
            },
            {
                "index_interval_start": 440,
                "index_interval_end": 478,
                "revealed_score": 1,
            },
            {
                "index_interval_start": 478,
                "index_interval_end": 478,
                "revealed_score": 0,
            }
        ]
    }
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    elif request.method == "GET":
        response = make_response(paragraph)
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response
    else:
        return make_response("Unknown method.")


@app.route("/api/v1/post-paragraph", methods=["POST", "OPTIONS"])
def post_paragraphs():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    elif request.method == "POST":
        database_service.add_paragraph(request.get_json(force=True))
        return make_response("Post paragraph successful.")
    else:
        return make_response("Unknown method.")

@app.route("/api/v1/post-sentence-to-parallel", methods=["POST", "OPTIONS"])
def post_sentence_to_parallel():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    elif request.method == "POST":
        database_service.add_sentence(request.get_json(force=True))
        return make_response("Post sentence to parallel successful.")
    else:
        return make_response("Unknown method.")

# change reveal score

# get one paragraph

# get multiple paragraphs
# login signup
