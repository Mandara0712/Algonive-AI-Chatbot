from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Enhanced FAQ dictionary with banking, support, and healthcare
faq = {
    # Greetings
    "hello": "Hello! I'm your virtual assistant. How can I help you today?",
    "hi": "Hi there! How can I assist you today?",
    "hey": "Hello! What can I help you with today?",
    
    # Banking
    "balance": "To check your account balance, please log in to your online banking or mobile app.",
    "transaction": "You can view your recent transactions in the 'Transactions' section of your banking app.",
    "card": "For card-related queries, please call our 24/7 card services at 1-800-XXX-XXXX.",
    "transfer": "You can transfer money between your accounts or to other payees through the 'Transfers' section in your banking app.",
    "loan": "For information about loans, please visit our website or call our loan department at 1-800-XXX-XXXX.",
    
    # Customer Support
    "return": "For returns or exchanges, please bring the item with original packaging and receipt to any of our stores.",
    "refund": "Refunds are typically processed within 5-7 business days after we receive your returned item.",
    "track order": "Please provide your order number and I'll check the status for you.",
    "store": "You can find our nearest store by visiting our website and using the store locator.",
    "contact": "You can reach our customer service at 1-800-XXX-XXXX or email support@example.com.",
    
    # Healthcare
    "appointment": "To schedule an appointment, please call our scheduling department at 1-800-XXX-XXXX or book online through our patient portal.",
    "doctor": "You can find information about our doctors and their specialties on our website.",
    "prescription": "For prescription refills, please contact your pharmacy directly or request through our patient portal.",
    "emergency": "If this is a medical emergency, please call 911 or go to the nearest emergency room immediately.",
    "billing": "For billing inquiries, please call our billing department at 1-800-XXX-XXXX.",
    
    # General
    "help": "I can assist you with banking services, customer support, and healthcare information. What do you need help with?",
    "thanks": "You're welcome! Is there anything else I can help you with?",
    "goodbye": "Thank you for chatting with us. Have a great day!"
}

def chatbot_response(user_input: str) -> str:
    text = user_input.lower()

    # --- Banking Responses ---
    if any(word in text for word in ["balance", "account", "money", "bank"]):
        if "balance" in text:
            return "Your current account balance can be viewed in the 'Accounts' section of your banking app. For security, we don't display sensitive information here."
        elif "transaction" in text or "history" in text:
            return "You can view your transaction history in the 'Transactions' tab of your banking app. How far back would you like to see?"
        elif "card" in text or "debit" in text or "credit" in text:
            return "For card-related assistance, please call our 24/7 card services at 1-800-XXX-XXXX. Is there anything else I can help with?"
        elif "transfer" in text or "send money" in text:
            return "You can transfer money between your accounts or to other payees through the 'Transfers' section in your banking app. Would you like instructions on how to set up a new payee?"
        elif "loan" in text or "mortgage" in text:
            return "For loan-related inquiries, please visit our website or call our loan department at 1-800-XXX-XXXX. Our representatives are available Monday-Friday, 9am-5pm EST."

    # --- Customer Support Responses ---
    elif any(word in text for word in ["order", "return", "refund", "product", "support"]):
        if "track" in text or "where is" in text:
            order_id = ''.join(filter(str.isdigit, text))
            if order_id:
                return f"Your order #{order_id} is on its way! Expected delivery is within 3-5 business days."
            return "Please provide your order number so I can check the status for you."
        elif "return" in text or "exchange" in text:
            return "You can return items within 30 days of purchase with a receipt. Would you like to know more about our return policy?"
        elif "store" in text or "location" in text:
            return "You can find our nearest store by visiting our website and using the store locator. Would you like me to provide a link?"
        elif "contact" in text or "speak" in text:
            return "You can reach our customer service at 1-800-XXX-XXXX or email support@example.com. Our representatives are available 24/7 to assist you."

    # --- Healthcare Responses ---
    elif any(word in text for word in ["appointment", "doctor", "prescription", "medical", "health"]):
        if "appointment" in text or "schedule" in text:
            return "To schedule an appointment, please call our scheduling department at 1-800-XXX-XXXX. Our representatives are available Monday-Friday, 8am-8pm EST."
        elif "prescription" in text or "refill" in text:
            return "For prescription refills, please contact your pharmacy directly or request through our patient portal. Do you need the link to the patient portal?"
        elif "symptom" in text or "pain" in text:
            return "I'm not a medical professional, but I can help you schedule an appointment with a doctor. For urgent medical concerns, please contact your healthcare provider or visit urgent care."
        elif "billing" in text or "insurance" in text:
            return "For billing or insurance questions, please call our billing department at 1-800-XXX-XXXX, Monday-Friday, 9am-5pm EST."

    # --- Check FAQ ---
    for key, value in faq.items():
        if key in text:
            return value

    # --- Default Response ---
    return "I'm not sure I understand. Could you please rephrase your question? I can help with banking, customer support, and healthcare-related questions."
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
            
        data = request.get_json()
        user_input = data.get('message', '').strip()
        
        if not user_input:
            return jsonify({'response': 'Please provide a message'})
            
        response = chatbot_response(user_input)
        return jsonify({'response': response})
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({'response': 'An error occurred while processing your request'}), 500

if __name__ == "__main__":
    app.run(debug=True)

