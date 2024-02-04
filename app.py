from flask import Flask, request, jsonify

app = Flask(__name__)


# Endpoint to respond to user messages
@app.route("/respond", methods=["POST"])
def respond_to_user():
    if request.method == "POST":
        data = request.get_json()
        user_message = data.get("message")
        reply = llama(user_message)
        response = {"response": reply}
        return jsonify(response), 200


# Endpoint to submit a completed conversation
@app.route("/submit_conversation", methods=["POST"])
def submit_conversation():
    if request.method == "POST":
        data = request.get_json()
        conversation = data.get("conversation")
        # Process the conversation here
        # For demonstration, we'll just acknowledge the submission
        response = {"status": "Conversation submitted successfully"}
        return jsonify(response), 200


if __name__ == "__main__":
    app.run(debug=True)
