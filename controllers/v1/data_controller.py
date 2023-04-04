import logging

from flask import make_response, request

from app import app
from services import database_service


def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


@app.route("/")
def hello_world():
    return "<p>API works.</p>"


@app.route("/api/v1/get-paragraph", methods=["GET", "OPTIONS"])
def get_paragraph():
    paragraph = {
        'title_interval_start': 439,
        'title_interval_end': 476,
        "paragraph": "Through decades that ran like rivers, endless rivers of endless woes. Through pick and shovel sjambok and jail. O such a long long journey! When the motor-car came, the sledge and the ox-cart began to die. But for a while the bicycle made in Britain, was the dream of every village boy. With the arrival of the bus, the city was brought into the village, and we began to yearn for the place behind the horizons. Such a long travail it was. A long journey from bush to concrete. ",
        "id": "flG47F77IQ",
        "creator_id": "vjakukfe",
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
            }
        ]
    }
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    elif request.method == "GET":
        return paragraph
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

# change reveal score

# get one paragraph

# get multiple paragraphs



# (login signup) or several dummy accounts just for prototype demo if easier?
