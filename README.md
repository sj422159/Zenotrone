# **MindMentor- Zenotrone**
## **Generative AI Chatbot -Doubt Solver Project Documentation**

## **Introduction**
This project is a FastAPI-based AI chatbot that allows users to upload PDFs, ask questions about the content, and receive AI-generated responses based on their education level. The chatbot uses a **Retrieval-Augmented Generation (RAG) system** with **Mistral AI** and **PostgreSQL (Supabase)** to enhance response accuracy and context relevance. Additionally, it features a **multi-personality AI** integrated alongside the doubt solver, allowing users to interact with AI personalities tailored to different tones and engagement styles.

---

## **Features**
- **PDF Upload**: Extracts text from uploaded PDFs.
- **Summarization**: Generates a concise summary of the document.
- **AI-Based Q&A**: Answers user queries based on PDF content.
- **Retrieval-Augmented Generation (RAG)**: Enhances AI responses by retrieving relevant document sections from PostgreSQL.
- **Education-Level Customization**: Adjusts explanations for Undergraduate, Graduate, Masters, or Specialist users.
- **Multi-Personality AI**: Allows users to select different AI personalities for engagement.
- **Chat History Storage**: Saves user queries and AI responses in PostgreSQL (Supabase).
- **Chat History Retrieval**: Allows users to fetch past interactions.
- **Text-to-Speech (Optional)**: Converts AI responses into speech.

---

## **Technology Stack**
- **Backend**: FastAPI (Python)
- **AI Model**: Mistral AI
- **Database**: PostgreSQL (Supabase)
- **PDF Processing**: PyPDF
- **Vector Storage**: FAISS (for RAG implementation)
- **Multi-Personality AI Engine**: Custom Personality Framework
- **Speech Synthesis**: Pyttsx3
- **API Requests**: Requests Library

---

## **Installation & Setup**
### **1. Clone the Repository**
```bash
 git clone <repo-url>
 cd <project-folder>
```

### **2. Install Dependencies**
```bash
pip install fastapi pydantic mistralai pypdf uvicorn pyttsx3 requests python-dotenv faiss psycopg2
```

### **3. Run the Server**
```bash
uvicorn main:app --reload
```

The server will start at `http://127.0.0.1:8000`

---

## **API Endpoints**
### **1. Home**
- **Endpoint:** `GET /`
- **Description:** Checks if the server is running.
- **Response:** `{ "message": "FastAPI server is running!" }`

### **2. Upload PDF**
- **Endpoint:** `POST /upload/`
- **Description:** Extracts text from the uploaded PDF and stores it in PostgreSQL.
- **Request:**
  - **File:** `UploadFile`
- **Response:**
```json
{
  "message": "PDF processed successfully",
  "summary": "This document discusses..."
}
```

### **3. Summarize PDF**
- **Endpoint:** `GET /summarize/`
- **Description:** Returns a summary of the uploaded PDF using RAG.
- **Response:** `{ "summary": "This document explains..." }`

### **4. Ask a Question**
- **Endpoint:** `POST /query/`
- **Description:** Answers user queries based on the uploaded PDF and education level using RAG with PostgreSQL.
- **Request:**
```json
{
  "query": "Explain neural networks",
  "education_level": "graduate"
}
```
- **Response:**
```json
{
  "response": "Neural networks are inspired by the human brain..."
}
```

### **5. Retrieve Chat History**
- **Endpoint:** `GET /history/`
- **Description:** Fetches the last 10 chat history records from PostgreSQL.
- **Response:**
```json
{
  "history": [
    { "user_query": "What is AI?", "ai_response": "AI stands for Artificial Intelligence..." },
    { "user_query": "Explain deep learning", "ai_response": "Deep learning is a subset of machine learning..." }
  ]
}
```

### **6. Select AI Personality**
- **Endpoint:** `POST /select_personality/`
- **Description:** Allows users to select an AI personality for interaction.
- **Request:**
```json
{
  "personality": "friendly"
}
```
- **Response:**
```json
{
  "message": "Personality set to friendly."
}
```

---

## **Workflow Overview**
- **Start FastAPI Server**
  - Initialize FastAPI, Mistral AI, and PostgreSQL (Supabase).
- **Upload PDF (`/upload/`)**
  - Extract text and store it in PostgreSQL.
  - Generate a summary using RAG.
- **Process Query (`/query/`)**
  - Get user question & education level.
  - Retrieve relevant document sections using FAISS & PostgreSQL.
  - Modify prompt & get AI response.
  - Store chat history in PostgreSQL.
- **Select AI Personality (`/select_personality/`)**
  - Allow users to customize AI interaction style.
- **Retrieve Data**
  - Fetch summary (`/summarize/`).
  - Fetch chat history (`/history/`).
- **(Optional) Convert AI Response to Speech**

---

## **Future Enhancements**
- **Improve RAG system by implementing more advanced document retrieval methods.**
- **Enhance UI with a frontend framework like React or Vue.js.**
- **Optimize query response time with better indexing techniques.**
- **Add multi-user authentication for personalized chat history.**
- **Expand AI personality options for more dynamic user interactions.**
