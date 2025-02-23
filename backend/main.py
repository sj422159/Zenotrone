from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pypdf import PdfReader
import time
import pyttsx3
import requests
from mistralai import Mistral
import os
from dotenv import load_dotenv
from pydantic import BaseModel


# Load environment variables
load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = "11RZDmjfsCHWP2QIcJPc9GrZ9LLrVfb8"
model = "mistral-small-latest"
client = Mistral(api_key=api_key)

SUPABASE_URL = "https://wougyfejtrikufucnwen.supabase.co"

SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYW5vbiIsImlhdCI6MTYzNjQwNjYwOCwiZXhwIjoxOTUxOTgyNjA4fQ.7"

# Store extracted PDF content
document_text = ""

# Define Request Model
class QueryRequest(BaseModel):
    query: str
    education_level: str  # Undergraduate, Graduate, Masters, Specialist

class ChatRequest(BaseModel):
    query: str
    mode: str  # Options: "funny", "supportive", "sarcastic"

@app.get("/")
def home():
    return {"message": "FastAPI server is running!"}

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    """Handles PDF upload and extracts text."""
    global document_text
    try:
        reader = PdfReader(file.file)
        document_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return {"message": "PDF processed successfully", "summary": summarize_pdf()}
    except Exception as e:
        return {"error": str(e)}

@app.post("/query/")
async def chat_with_pdf(request: QueryRequest):
    """Answers user queries based on uploaded PDF and education level."""
    if not document_text:
        return {"response": "No PDF content available. Please upload a PDF first."}

    # Modify response based on education level
    education_prompt = {
        "undergraduate": "Explain in simple terms with examples.",
        "graduate": "Give a structured explanation with key concepts.",
        "masters": "Provide an in-depth analysis using advanced terms.",
        "specialist": "Use technical language and detailed reasoning."
    }

    level_prompt = education_prompt.get(request.education_level.lower(), "Explain in a clear way.")

    messages = [
        {"role": "user", "content": f"Based on this document: {document_text}\n"
                                        f"Answer this question: {request.query}\n"
                                        f"{level_prompt}"}
    ]

    response = make_request(messages)

    # Save chat history to Supabase
    save_chat_to_supabase(request.query, response)

    return {"response": response}

@app.get("/summarize/")
def summarize_pdf():
    """Summarizes the uploaded PDF."""
    if not document_text:
        return {"error": "No PDF content available."}

    messages = [{"role": "user", "content": f"Summarize this document: {document_text}"}]
    return make_request(messages)

@app.get("/history/")
def get_chat_history():
    """Fetches the last 10 chat history records from Supabase."""
    headers = {"apikey": SUPABASE_API_KEY, "Authorization": f"Bearer {SUPABASE_API_KEY}"}
    response = requests.get(f"{SUPABASE_URL}/rest/v1/chats?select=user_query,ai_response&order=created_at.desc&limit=10", headers=headers)

    if response.status_code == 200:
        return {"history": response.json()}
    return {"error": "Failed to fetch chat history"}

@app.post("/chat/")
async def chat_best_friend(request: ChatRequest):
    """Acts like a best friend and responds based on Funny, Supportive, or Sarcastic mode."""
    mode_responses = {
        "funny": "Respond in a hilarious, light-hearted way like a best friend cracking jokes.",
        "supportive": "Give comforting words, mental health advice, and meditation techniques like a caring best friend.",
        "sarcastic": "Respond in a witty, savage, and slightly mocking way like a best friend roasting you but in a fun way."
    }

    mode_prompt = mode_responses.get(request.mode.lower(), "Be a supportive and friendly chatbot.")

    messages = [
        {"role": "user", "content": f"{mode_prompt}\nUser: {request.query}"}
    ]

    response = make_request(messages)

    return {"response": response}


def retrieve_relevant_context(query):
    """Finds the most relevant document chunks using cosine similarity."""
    if not tfidf_matrix:
        return ""
    
    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    top_indices = np.argsort(similarities)[-3:][::-1]  # Get top 3 relevant sentences
    
    relevant_text = " ".join([document_chunks[i] for i in top_indices])
    return relevant_text

def save_chat_to_supabase(question, response):
    """Stores chat history in Supabase."""
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {"user_query": question, "ai_response": response}
    requests.post(f"{SUPABASE_URL}/rest/v1/chats", json=data, headers=headers)

def make_request(messages):
    """Handles API calls to Mistral AI with retry logic."""
    while True:
        try:
            chat_response = client.chat.complete(model=model, messages=messages)
            return chat_response.choices[0].message.content.strip()
        except Exception as e:
            if "429" in str(e):  # Rate limit exceeded
                time.sleep(5)
            else:
                return f"Error from AI: {str(e)}"

def text_to_speech(text: str):
    """Converts text to speech using pyttsx3."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()



