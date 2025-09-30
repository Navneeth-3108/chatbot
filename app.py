from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt = (
    "You are a smart assistant chatbot for an Expiry Date Tracker application designed for the Smart India Hackathon 2025.\n\n"
    "Your role is to help customers and retailers understand how the app works, how to track expiry dates of products, and how the automation process benefits them.\n\n"
    "The solution involves two portals:\n\n"
    "1. Customer Portal:\n"
    "   - Users sign up with phone and email.\n"
    "   - After purchase, their product details (with expiry dates) are auto-added to their account.\n"
    "   - Smart notifications are sent starting 2 weeks before expiry to reduce food and medicine wastage.\n\n"
    "2. Retailer Portal:\n"
    "   - Stock is updated upon arrival.\n"
    "   - Billing system has an internal expiry column.\n"
    "   - When a bill is generated, the customer app syncs product and expiry info.\n\n"
    "The system uses Barcode + OCR technology to extract expiry dates from products that only have standard UAN barcodes (not GS1/2D), solving a real-world problem.\n\n"
    "Your job is to:\n"
    "- Answer user questions clearly.\n"
    "- Explain how the app works.\n"
    "- Emphasize the benefits of automated reminders and expiry tracking.\n"
    "- Never invent product data; guide the user to contact support or check the product if details are missing.\n\n"
    "Target audience: general consumers and small/medium retailers in India.\n"
    "Use simple, clear language."
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message or not isinstance(user_message, str):
        return jsonify({"error": "Invalid input"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {"role": "user", "content": user_message}
            ]
        )
        bot_reply = response.choices[0].message.content
        return jsonify({"response": bot_reply})
    except Exception:
        # For production, avoid exposing internal errors
        return jsonify({"error": "Server error"}), 500

# Sample list of Expirex-related questions for suggestions
SUGGESTIONS = [
    "How does the Expiry Date Tracker app work?",
    "How do I add a new product to my account?",
    "How are expiry dates detected automatically?",
    "What notifications will I receive before expiry?",
    "How does the retailer portal update stock?",
    "How does barcode and OCR technology work in Expirex?",
    "How do I sign up as a customer?",
    "How do I sign up as a retailer?",
    "What should I do if my product's expiry date is missing?",
    "How does Expirex help reduce wastage?",
]

@app.route("/suggest", methods=["GET"])
def suggest():
    query = request.args.get("q", "").strip().lower()
    if not query:
        # Return top 5 suggestions if no query is provided
        return jsonify({"suggestions": SUGGESTIONS[:5]})
    # Filter suggestions containing the query (case-insensitive)
    filtered = [s for s in SUGGESTIONS if query in s.lower()]
    # Return up to 5 suggestions
    return jsonify({"suggestions": filtered[:5]})

if __name__ == "__main__":
    app.run(debug=True)
