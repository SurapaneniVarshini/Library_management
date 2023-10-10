import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient
from datetime import datetime
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import io

from tkinter import messagebox

# MongoDB connection settings
MONGO_CONNECTION_STRING = "mongodb+srv://varshinisurapaneni0211:varshini1234@clusterlibrary.1vvke4p.mongodb.net/library_management_system"

DB_NAME = "library_management_system"
COLLECTION_BOOKS = "books"
COLLECTION_BORROWERS = "borrowers"

def get_all_borrower_details():
    # Retrieve all borrower details from the collection
    client = MongoClient(MONGO_CONNECTION_STRING)
    db = client[DB_NAME]
    collection = db[COLLECTION_BORROWERS]
    borrower_details = list(collection.find({}))
    client.close()
    return borrower_details

def update_book_copies(book_id, num_copies):
    # Update the copies_available field in the books collection
    client = MongoClient(MONGO_CONNECTION_STRING)
    db = client[DB_NAME]
    collection = db[COLLECTION_BOOKS]
    collection.update_one({"book_id": book_id}, {"$set": {"copies_available": num_copies}})
    client.close()

def display_borrower_details():
    # Retrieve all borrower details
    borrower_details = get_all_borrower_details()

    # Create a new window to display borrower details
    window = tk.Tk()
    window.title("Borrower Details")

    # Create a Treeview widget to display borrower details in tabular format
    tree = ttk.Treeview(window)
    tree["columns"] = ("Book ID", "Book Name", "Author Name", "Borrower ID", "From Date", "To Date", "Checkout Date", "Returned", "Returned Date")

    # Define column headings
    tree.heading("#1", text="Book ID")
    tree.heading("#2", text="Book Name")
    tree.heading("#3", text="Author Name")
    tree.heading("#4", text="Borrower ID")
    tree.heading("#5", text="From Date")
    tree.heading("#6", text="To Date")
    tree.heading("#7", text="Checkout Date")
    tree.heading("#8", text="Returned")
    tree.heading("#9", text="Returned Date")

    # Insert borrower details into the Treeview widget
    for borrower in borrower_details:
        tree.insert("", "end", values=(
            borrower["book_id"],
            borrower["book_name"],
            borrower["author_name"],
            borrower["borrower_id"],
            borrower["from_date_time"],
            borrower["to_date_time"],
            borrower["checkout_datetime"],
            borrower.get("returned", ""),
            borrower.get("returned_date_time", "")
        ))

    tree.pack(expand=True, fill="both")

    # Return button
    btn_return = tk.Button(window, text="Return", command=lambda: on_return(tree))
    btn_return.pack()

    window.mainloop()

def on_return(tree):
    # Get the selected item's values from the Treeview widget
    selected_item = tree.selection()[0]
    values = tree.item(selected_item, "values")

    # Get current date and time
    returned_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Update the "Returned" and "Returned Date" fields in the record
    client = MongoClient(MONGO_CONNECTION_STRING)
    db = client[DB_NAME]
    collection = db[COLLECTION_BORROWERS]

    returned = "True" if values[7] == "False" else "False"
    collection.update_one({"book_id": values[0]}, {"$set": {"returned": returned, "returned_date_time": returned_date_time}})
    client.close()

    # Update the Treeview widget with the new values
    tree.item(selected_item, values=values[:-2] + (returned, returned_date_time))

    # Add the returned book's count back to the copies_available field of the respective book in the books collection
    book_id = values[0]
    book_client = MongoClient(MONGO_CONNECTION_STRING)
    book_db = book_client[DB_NAME]
    book_collection = book_db[COLLECTION_BOOKS]
    book = book_collection.find_one({"book_id": book_id})
    book_client.close()

    copies_available = book["copies_available"]
    copies_available = int(copies_available) + 1
    update_book_copies(book_id, copies_available)

    # Show a popup message for successful return
    messagebox.showinfo("Return Successful", f"Book ID: {book_id} successfully returned.")


if __name__ == "__main__":
    display_borrower_details()
