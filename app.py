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
    "Can I export my product list?",
    "How do I reset my password?",
    "Is there a mobile app for Expirex?",
    "How do I contact support?",
    "Can I track multiple stores with one account?",
    "How do I delete a product?",
    "How do I update product details?",
    "What data does Expirex collect?",
    "Is my data secure with Expirex?",
    "How do I enable notifications?",
    "How do I change my email address?",
    "Can I integrate Expirex with other inventory systems?",
    "How do I view expired products?",
    "How do I set custom expiry alerts?",
    "How do I invite team members?",
    "Can I use Expirex offline?",
    "How do I get analytics or reports?",
    "What happens when a product expires?",
    "How do I filter products by expiry date?",
    "How do I recover a deleted product?",
    "How do I change my subscription plan?",
    "How do I update billing information?",
    "Can I bulk upload products?",
    "How do I log out?",
    "How do I switch between customer and retailer mode?",
    "How do I print my inventory list?",
    "How do I set up barcode scanning?",
    "How do I get notified about soon-to-expire products?",
    "How do I manage product categories?",
    "How do I search for a product?",
    "How do I mark a product as sold or disposed?",
    "How do I get started with Expirex?",
    "What browsers are supported?",
    "How do I report a bug or issue?",
    "How do I access Expirex tutorials?",
    "How do I customize notification times?",
    "How do I pause notifications?",
    "How do I transfer ownership of my account?",
    "How do I merge duplicate products?",
    "How do I set up two-factor authentication?",
    "How do I view my account activity?",
    "How do I restore a previous inventory backup?",
    "How do I request a new feature?",
    "How do I check for app updates?",
    "How do I manage user permissions?",
    "How do I set up automatic backups?",
    "How do I use Expirex for perishable goods?",
    "How do I get a demo of Expirex?",
    "How do I change the language of the app?",
    "How do I access Expirex on different devices?",
    "How do I manage notifications for different products?",
    "How do I set up recurring products?",
    "How do I view product history?",
    "How do I archive old products?",
    "How do I set up reminders for product restocking?",
    "How do I use Expirex for medicines?",
    "How do I use Expirex for food items?",
    "How do I use Expirex for cosmetics?",
    "How do I use Expirex for chemicals?",
    "How do I use Expirex for electronics?",
    "How do I use Expirex for retail stores?",
    "How do I use Expirex for warehouses?",
    "How do I use Expirex for restaurants?",
    "How do I use Expirex for pharmacies?",
    "How do I use Expirex for supermarkets?",
    "How do I use Expirex for small businesses?",
    "How do I use Expirex for large enterprises?",
    "How do I use Expirex for personal use?",
    "How do I use Expirex for schools?",
    "How do I use Expirex for hospitals?",
    "How do I use Expirex for laboratories?",
    "How do I use Expirex for logistics?",
    "How do I use Expirex for supply chain management?",
    "How do I use Expirex for government organizations?",
    "How do I use Expirex for NGOs?",
    "How do I use Expirex for research institutions?",
    "How do I use Expirex for event management?",
    "How do I use Expirex for catering services?",
    "How do I use Expirex for hotels?",
    "How do I use Expirex for bakeries?",
    "How do I use Expirex for dairy farms?",
    "How do I use Expirex for meat processing?",
    "How do I use Expirex for beverage companies?",
    "How do I use Expirex for florists?",
    "How do I use Expirex for pet stores?",
    "How do I use Expirex for cleaning services?",
    "How do I use Expirex for automotive parts?",
    "How do I use Expirex for construction materials?",
    "How do I use Expirex for office supplies?",
    "How do I use Expirex for art supplies?",
    "How do I use Expirex for sports equipment?",
    "How do I use Expirex for gardening supplies?",
    "How do I use Expirex for seasonal products?",
    "How do I use Expirex for promotional items?",
    "How do I use Expirex for limited edition products?"
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
