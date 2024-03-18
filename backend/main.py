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
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import docx
from typing import Union
import io
from fastapi import Request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import pymongo
import fitz  
import os


class Response(BaseModel):
    result: str | None


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize NLTK resources
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


def perform_operation(csv_content: pd.DataFrame, question: str) -> str:
    # Tokenize and preprocess the question
    question_tokens = word_tokenize(question.lower())
    question = ' '.join([lemmatizer.lemmatize(word) for word in question_tokens])
    
    # Define mappings for different operations and their synonyms
    operation_mappings = {
        "maximum": ["max", "maximum"],
        "minimum": ["min", "minimum"],
        "average": ["avg", "average"],
        "sum": ["sum", "add", "addition", "total"],
        "multiply": ["multiply", "product", "multiplication"],
        "compare": ["compare", "comparison", "difference"],
        "row_performance": ["performance", "values", "metrics"]
    }
    
    # Determine the operation and column/row name
    operation = None
    target_name = None
    
    # Check for specific operations
    for op, aliases in operation_mappings.items():
        if any(alias in question for alias in aliases):
            operation = op
            break
    
    if operation is None:
        return "Unsupported operation. Please ask a valid question."
    
    # Check for column or row-based operation
    if " in column " in question:
        operation_target = "column"
    elif " in row " in question:
        operation_target = "row"
    else:
        return "Invalid question format. Please specify the operation and target using 'operation in target target_name' format."
    
    # Extract the target name (column/row name)
    target_index = question.find(" in " + operation_target + " ")
    target_name = question[target_index + len(" in " + operation_target + " "):].strip()
    
    # Perform the requested operation
    if operation_target == "column":
        if operation == "maximum":
            max_value = csv_content[target_name].max()
            result = f"The maximum value in {operation_target} '{target_name}' is {max_value}."
        elif operation == "minimum":
            min_value = csv_content[target_name].min()
            result = f"The minimum value in {operation_target} '{target_name}' is {min_value}."
        elif operation == "average":
            avg_value = csv_content[target_name].mean()
            result = f"The average value in {operation_target} '{target_name}' is {avg_value:.2f}."
        elif operation == "sum":
            sum_value = csv_content[target_name].sum()
            result = f"The sum of values in {operation_target} '{target_name}' is {sum_value:.2f}."
        elif operation == "multiply":
            # Perform element-wise multiplication of the column
            product = csv_content[target_name].prod()
            result = f"The product of values in {operation_target} '{target_name}' is {product:.2f}."
        else:
            result = "Unsupported operation for columns."
    elif operation_target == "row":
        # For row-based operations (e.g., comparisons)
        if operation == "compare":
            # Extract row indices
            indices = [int(s) for s in question.split() if s.isdigit()]
            if len(indices) != 2:
                return "Invalid row indices. Please provide exactly two row indices to compare."
            
            # Extract row values
            row_values = csv_content.iloc[indices].values
            if row_values.shape[0] != 2:
                return "Invalid row indices. Please provide valid row indices to compare."
            
            # Perform comparison
            comparison_result = row_values[0] - row_values[1]
            result = f"Comparison result between rows {indices[0]} and {indices[1]}: {comparison_result}."
        elif operation == "row_performance":
            # Perform calculations for row performance metrics
            row_metrics = csv_content.mean(axis=1)  # Example: Mean of values in each row
            result = f"Performance metrics for rows: {row_metrics}."
        else:
            result = "Unsupported operation for rows."

    return result


def save_csv_to_backend_storage(file: UploadFile) -> str:
    # Save the uploaded CSV file to backend storage
    file_path = os.path.join(os.getcwd(), file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    return file_path


# Function to extract text content from DOCX files
def extract_text_from_docx(file: UploadFile) -> str:
    # Read the file content from the UploadFile object
    file_content = file.file.read()
    
    # Create a docx.Document object from the file content
    doc = docx.Document(io.BytesIO(file_content))
    
    # Extract text from the document
    text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
    return text



def extract_text_from_pdf(file: UploadFile) -> str:
    text = ""
    pdf_bytes = file.file.read()
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        page_text = page.get_text()
        text += page_text + ""
    
    return text


def process_uploaded_file(file: UploadFile, question: str) -> str:
    print("Question from frontend:", question)
    # Initialize NLTK resources
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    # Check if the question is a greeting or basic NLP query
    if question is None:
        return "Hi there! Please upload your file."
    elif any(greeting in question.lower() for greeting in ["hi", "hello", "hey"]):
        return "Hello! Please upload your file."
    elif "how are you" in question.lower():
        return "I'm fine, thank you! How can I help you?"
    elif "who are you" in question.lower():
        return "I am a ChatBot designed to assist you with your queries. Please feel free to ask any questions!"   
    
    # Check the file extension
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension == "pdf":
        # Extract text content from PDF file
        file_content = extract_text_from_pdf(file)
    elif file_extension == "docx":
        # Extract text content from DOCX file
        file_content = extract_text_from_docx(file)
    elif file_extension == "csv":
        # Save the uploaded CSV file to backend storage
        file_path = save_csv_to_backend_storage(file)
        # Read the uploaded CSV file content
        csv_content = pd.read_csv(file_path)
        # Perform operation based on the question
        result = perform_operation(csv_content, question)
        # Delete the file from storage after processing
        os.remove(file_path)
        return result

    elif file_extension== "txt":
        file_content = file.file.read().decode("utf-8")
       
    else:
        # Unsupported file type
        return "Unsupported file type. Please upload a PDF, DOCX, or CSV file."
    
    # Convert the content to .txt format and save it
    with open("uploaded_file.txt", "w", encoding="utf-8") as txt_file:
        txt_file.write(file_content)
    
    # Now, read the .txt file and perform further processing
    with open("uploaded_file.txt", "r", encoding="utf-8") as txt_file:
        file_content = txt_file.readlines()  # Read lines instead of the whole content
    
    # Initialize an empty list to store relevant lines
    relevant_lines = []
    
    if question is not None:
        # Tokenize and preprocess the question
        question_tokens = word_tokenize(question.lower())
        question = ' '.join([lemmatizer.lemmatize(word) for word in question_tokens if word not in stop_words])
        
        # Tokenize and preprocess each line in the file content
        preprocessed_lines = []
        for line in file_content:
            words = word_tokenize(line.lower())  # Tokenize each line into words
            filtered_words = [word for word in words if word not in stop_words]
            preprocessed_lines.append(' '.join([lemmatizer.lemmatize(word) for word in filtered_words]))
        
        # Calculate TF-IDF vectors for the question and lines
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([question] + preprocessed_lines)
        
        # Compute cosine similarity between the question and each line
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]
        
        # Select lines with cosine similarity greater than 0.5
        for idx, sim in enumerate(similarities):
            if sim > 0.3:
                relevant_lines.append(file_content[idx].strip()) 
    else:
        # If question is not provided, consider all lines as relevant
        return "The question asked is not guaranteed to be in the uploaded document. Try some another questions!!" 
    
    # Concatenate the relevant lines to form the response
    response = "\n\n".join(relevant_lines)
    os.remove("uploaded_file.txt")
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