from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import PyPDF2
import docx
from typing import Union
import io
from fastapi import Request


# Load environment variables from .env file (if any)
# load_dotenv()

class Response(BaseModel):
    result: str | None

# Define the allowed origins for CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

# Create an instance of FastAPI
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to extract text content from DOCX files
def extract_text_from_docx(file: UploadFile) -> str:
    # Read the file content from the UploadFile object
    file_content = file.file.read()
    
    # Create a docx.Document object from the file content
    doc = docx.Document(io.BytesIO(file_content))
    
    # Extract text from the document
    text = "\n\n\n".join(paragraph.text for paragraph in doc.paragraphs)
    return text

# Function to extract text content from PDF files
def extract_text_from_pdf(file: UploadFile) -> str:
    pdf_reader = PyPDF2.PdfReader(file.file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text = text + pdf_reader.pages[page_num].extract_text() 
    return text

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Initialize NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def process_uploaded_file(file: UploadFile, question: str) -> str:
    print("Question from frontend:", question)
    # Initialize NLTK resources
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    
    # Check the file extension
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension == "pdf":
        # Extract text content from PDF file
        file_content = extract_text_from_pdf(file)
    elif file_extension == "docx":
        # Extract text content from DOCX file
        file_content = extract_text_from_docx(file)
    else:
        # Read the uploaded file content as plain text
        file_content = file.file.read().decode("utf-8")
    
    # Tokenize the file content into sentences
    sentences = sent_tokenize(file_content)
    
    # Tokenize the file content into paragraphs or lines
    paragraphs = [paragraph.strip() for paragraph in file_content.split('\n') if paragraph.strip()]
    
    # Initialize an empty list to store relevant paragraphs
    relevant_paragraphs = []
    
    if question is not None:
        # Tokenize and preprocess the question
        question_tokens = word_tokenize(question.lower())
        question = ' '.join([lemmatizer.lemmatize(word) for word in question_tokens if word not in stop_words])
        
        # Tokenize and preprocess each paragraph in the file content
        preprocessed_paragraphs = []
        for paragraph in paragraphs:
            words = word_tokenize(paragraph.lower())
            filtered_words = [word for word in words if word not in stop_words]
            preprocessed_paragraphs.append(' '.join([lemmatizer.lemmatize(word) for word in filtered_words]))
        
        # Calculate TF-IDF vectors for the question and paragraphs
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([question] + preprocessed_paragraphs)
        
        # Compute cosine similarity between the question and each paragraph
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]
        
        # Select paragraphs with cosine similarity greater than 0.8
        for idx, sim in enumerate(similarities):
            if sim > 0.8:
                relevant_paragraphs.append(paragraphs[idx])
        
        #Select top N paragraphs with highest cosine similarity
        top_n = min(len(paragraphs), 2)  # Select top 2 paragraphs at most
        top_indices = similarities.argsort()[-top_n:][::-1]
        
        relevant_paragraphs = [paragraphs[idx] for idx in top_indices]
    else:
        # If question is not provided, consider all paragraphs as relevant
        relevant_paragraphs = paragraphs
    
    # Concatenate the relevant paragraphs to form the response
    response = "\n\n".join(relevant_paragraphs)
    
    return response


# Endpoint to handle predictions
@app.post("/predict", response_model=Response)
async def predict(
    question: str = Form(None),
    file: UploadFile = File(...)
) -> Any:
    # Print the received question
    print("Received question:", question)

    # Call the function to process the uploaded file and handle user queries
    result = process_uploaded_file(file, question)
    print(result)
    return {"result": result}

