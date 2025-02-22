from flask import Flask, request, jsonify
from flask_cors import CORS
from mistralai import Mistral
from pypdf import PdfReader
import pyttsx3

app = Flask(__name__)
CORS(app)

# Mistral API Configuration
api_key = "YOUR_MISTRAL_API_KEY"
model = "mistral-small-latest"
client = Mistral(api_key=api_key)

# Store extracted PDF content
pdf_content = None

@app.route('/')
def home():
    return "Flask server is running with Mistral AI!"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = client.chat(model=model, messages=[{"role": "user", "content": user_message}])
        bot_reply = response.choices[0].message.content.strip()
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    global pdf_content
    if 'pdf' not in request.files:
        return jsonify({"error": "No PDF file uploaded"}), 400

    pdf_file = request.files['pdf']
    try:
        reader = PdfReader(pdf_file)
        pdf_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        pdf_content = pdf_text[:5000]
        return jsonify({"message": "PDF content extracted successfully", "summary": summarize_pdf()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def summarize_pdf():
    """Summarizes the extracted PDF content."""
    if not pdf_content:
        return "No PDF uploaded yet."

    messages = [{"role": "user", "content": f"Summarize this document: {pdf_content}"}]
    return make_request(messages)

def make_request(messages):
    """Handles API request with retry logic."""
    try:
        chat_response = client.chat(model=model, messages=messages)
        return chat_response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/text_to_speech', methods=['POST'])
def text_to_speech():
    """Converts text to speech."""
    data = request.json
    text = data.get("text", "")
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        return jsonify({"message": "Speech played successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
