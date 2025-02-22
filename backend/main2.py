from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pypdf import PdfReader
import time
import pyttsx3
from mistralai import Mistral

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize Mistral API
api_key = "11RZDmjfsCHWP2QIcJPc9GrZ9LLrVfb8"
model = "mistral-small-latest"
client = Mistral(api_key=api_key)

# Store extracted PDF content
document_text = ""

class QueryRequest(BaseModel):
    query: str
@app.route('/')
def home():
    return "Flask server is running!"

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    global document_text
    try:
        reader = PdfReader(file.file)
        document_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return {"message": "PDF processed successfully", "summary": summarize_pdf()}
    except Exception as e:
        return {"error": str(e)}

@app.post("/query/")
async def chat_with_pdf(request: QueryRequest):
    if not document_text:
        return {"response": "No PDF content available. Please upload a PDF first."}
    
    messages = [{"role": "user", "content": f"Based on this document: {document_text}\nAnswer this question: {request.query}"}]
    response = make_request(messages)
    return {"response": response}

@app.get("/summarize/")
def summarize_pdf():
    if not document_text:
        return "No PDF content available."
    messages = [{"role": "user", "content": f"Summarize this document: {document_text}"}]
    return make_request(messages)

def make_request(messages):
    while True:
        try:
            chat_response = client.chat.complete(model=model, messages=messages)
            return chat_response.choices[0].message.content.strip()
        except Exception as e:
            if "429" in str(e):
                time.sleep(5)
            else:
                return str(e)

def text_to_speech(text: str):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
