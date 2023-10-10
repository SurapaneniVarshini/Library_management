from flask import Flask, render_template, request
from pymongo import MongoClient
import base64
import spacy

app = Flask(__name__)

# Load spaCy's pre-trained word embeddings model
nlp = spacy.load("en_core_web_lg")

# MongoDB connection settings
MONGO_CONNECTION_STRING = "mongodb+srv://varshinisurapaneni0211:varshini1234@clusterlibrary.1vvke4p.mongodb.net/library_management_system"

# Connect to MongoDB
client = MongoClient(MONGO_CONNECTION_STRING)
db = client["library_management_system"]
collection = db["books"]

# Route for the home page
@app.route("/")
def home():
    return render_template("index.html")

# Route for handling the search request
@app.route("/search", methods=["POST"])
def search():
    search_text = request.form.get("search_text")
    search_by = request.form.get("search_by")

    # Perform the book search based on the user's input
    if search_by == "Title":
        query = {"book_name": {"$regex": search_text, "$options": "i"}}
    elif search_by == "Author":
        query = {"author_name": {"$regex": search_text, "$options": "i"}}
    elif search_by == "Publisher":
        query = {"publisher": {"$regex": search_text, "$options": "i"}}
    else:
        query = {}

    # Convert the MongoDB cursor to a list
    books = list(collection.find(query))

    # Encode the book photo as base64 and add it to the book document
    for book in books:
        book_photo_binary = book["book_photo"]
        book_photo_base64 = base64.b64encode(book_photo_binary).decode("utf-8")
        book["book_photo"] = book_photo_base64

    # Calculate relevance scores using text similarity
    for book in books:
        title_similarity = nlp(search_text).similarity(nlp(book["book_name"]))
        author_similarity = nlp(search_text).similarity(nlp(book["author_name"]))
        relevance_score = (title_similarity + author_similarity) / 2
        book["relevance"] = relevance_score
        book["title_similarity"] = title_similarity
        book["author_similarity"] = author_similarity

    # Sort the books by relevance score in descending order
    books.sort(key=lambda x: x["relevance"], reverse=True)

    return render_template("results.html", books=books)

@app.route("/get_all_books", methods=["GET"])
def get_all_books():
    # Retrieve all books from the database
    all_books = list(collection.find())

    # Encode the book photos as base64 and add them to the book documents
    for book in all_books:
        book_photo_binary = book["book_photo"]
        book_photo_base64 = base64.b64encode(book_photo_binary).decode("utf-8")
        book["book_photo"] = book_photo_base64

    return render_template("all_books.html", books=all_books)

if __name__ == "__main__":
    app.run(debug=True)
