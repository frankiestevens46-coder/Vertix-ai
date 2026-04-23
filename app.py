from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").lower()
        
        if "hello" in user_message:
            bot_response = "Hey! 👋 What can I help you with today?"
        elif "coding" in user_message:
            bot_response = "I love coding! What language are we working in? ⚡"
        else:
            bot_response = "Vertix AI is now running on the Cloud! 🚀"
            
        return jsonify({"response": bot_response})
    except Exception as e:
        return jsonify({"response": "Error in logic. Check Render logs! ⚡"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
