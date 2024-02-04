from flask import Flask, request, jsonify
from llm import respond_to_user, generate_facts, insert_facts

app = Flask(__name__)

@app.route("/hello", methods=["GET"])
def hello_world():
    return jsonify({"message": "Hello, WikiLLM!"}), 200


# Endpoint to respond to user messages
@app.route("/respond", methods=["POST"])
def respond_to_user():
    if request.method == "POST":
        data = request.get_json()
        conversation = data.get("conversation")
        reply = respond_to_user(conversation)
        response = {"response": reply}
        return jsonify(response), 200


# Endpoint to submit a completed conversation
@app.route("/submit_conversation", methods=["POST"])
def submit_conversation():
    if request.method == "POST":
        data = request.get_json()
        conversation = data.get("conversation")
        facts = generate_facts(conversation)
        insert_facts(facts)
        response = {"response": facts}
        return jsonify(response), 200


if __name__ == "__main__":
    app.run(debug=True)
