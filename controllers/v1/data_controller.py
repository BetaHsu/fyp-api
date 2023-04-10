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
    logging.info("call post paragraph")
    data = request.get_json(force=True)
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    elif request.method == "POST":
        logging.info("post_paragraph work" + data)
        response = make_response(database_service.add_paragraph(data))
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response
        # database_service.add_paragraph(request.get_json(force=True))
        # return make_response("Post paragraph successful.")
    else:
        return make_response("Unknown method.")


@app.route("/api/v1/post-sentence-to-parallel", methods=["POST", "OPTIONS"])
def post_sentence_to_parallel():
    data = request.get_json(force=True)
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    elif request.method == "POST":
        response = make_response(database_service.add_sentence(data))
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response
        # database_service.add_sentence(request.get_json(force=True))
        # return make_response("Post sentence to parallel successful.")
    else:
        return make_response("Unknown method.")


@app.route("/api/v1/add-user", methods=["POST", "OPTIONS"])
def add_user():
    data = request.get_json()
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    elif request.method == "POST":
        response = make_response(database_service.add_user(data))
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response
    else:
        return make_response("Unknown method.")


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

# login signup
@app.route("/api/v1/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        isSigningUp = request.form.get('isSigningUp', Flase, type=bool)
        # connect to the db
        user = "admin"
        password = os.getenv('MONGODBPASSWORD')
        client = MongoClient(
            "mongodb+srv://" + user + ":" + password + "@cluster0.xcvzv0m.mongodb.net/?retryWrites=true&w=majority",
            server_api=ServerApi('1'))
        # Get db
        db = client["fyp"]
        # Get collection
        collection = db["users"]

        if isSigningUp:
            # Perform sign-up
            collection.insert_one({'email': email, 'password': password})
            message = 'Successfully signed up'
        else:
            # Perform sign-in
            user = collection.find_one({'email': email, 'password': password})
            if user:
                message = 'Successfully signed in'
            else:
                message = 'Incorrect email or password'
        return jsonify({'message': message})
    return render_template('signup.html')

# get multiple paragraphs
# change reveal score
