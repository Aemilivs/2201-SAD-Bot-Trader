import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/health', methods=['GET'])
def health():
    return flask.jsonify({'healthy': True}), 200

app.run()
