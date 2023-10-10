import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from pymongo import MongoClient
import os

# MongoDB connection settings
MONGO_CONNECTION_STRING = "mongodb+srv://varshinisurapaneni0211:varshini1234@clusterlibrary.1vvke4p.mongodb.net/library_management_system"

DB_NAME = "library_management_system"
COLLECTION_NAME = "books"

def get_mongo_client():
    return MongoClient(MONGO_CONNECTION_STRING)

from PIL import Image, ImageTk
import io

# ...

def retrieve_book_details():
    book_id = entry_book_id.get()

    if not book_id:
        messagebox.showwarning("Incomplete Information", "Please enter the book ID.")
        return

    try:
        # Establish a connection to MongoDB
        client = get_mongo_client()
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Retrieve the book record from the collection based on the book ID
        book_record = collection.find_one({"book_id": book_id})

        if book_record:
            # Display the book details
            entry_book_name.delete(0, tk.END)
            entry_book_name.insert(0, book_record.get("book_name"))

            entry_author_name.delete(0, tk.END)
            entry_author_name.insert(0, book_record.get("author_name"))

            entry_copies_available.delete(0, tk.END)
            entry_copies_available.insert(0, book_record.get("copies_available"))

            # Display the book photo if available
            book_photo_bytes = book_record.get("book_photo")
            if book_photo_bytes:
                # Convert image bytes to Image object
                image = Image.open(io.BytesIO(book_photo_bytes))

                # Resize image if needed (optional)
                image = image.resize((100, 150))

                # Create a Tkinter PhotoImage from the Image object
                book_photo_tk = ImageTk.PhotoImage(image)

                # Set the PhotoImage to the label
                label_photo.config(image=book_photo_tk)
                label_photo.image = book_photo_tk  # Store a reference to prevent garbage collection

            # Show the "Delete" button
            delete_button.grid(row=6, columnspan=3)

        else:
            messagebox.showinfo("Book Not Found", "No book found with the specified ID.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

    finally:
        client.close()



def delete_book_record():
    book_id = entry_book_id.get()

    if not book_id:
        messagebox.showwarning("Incomplete Information", "Please enter the book ID.")
        return

    try:
        # Establish a connection to MongoDB
        client = get_mongo_client()
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Delete the book record from the collection based on the book ID
        result = collection.delete_one({"book_id": book_id})

        if result.deleted_count > 0:
            messagebox.showinfo("Success", "Book record deleted successfully.")
        else:
            messagebox.showinfo("Book Not Found", "No book found with the specified ID.")

        # Clear the entry fields and photo after deletion
        entry_book_id.delete(0, tk.END)
        entry_book_name.delete(0, tk.END)
        entry_author_name.delete(0, tk.END)
        entry_copies_available.delete(0, tk.END)
        label_photo.config(image="")
        delete_button.grid_remove()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

    finally:
        client.close()

# Create the main application window
root = tk.Tk()
root.title("Library Management System")

# Book ID
label_book_id = tk.Label(root, text="Book ID:")
label_book_id.grid(row=0, column=0)
entry_book_id = tk.Entry(root)
entry_book_id.grid(row=0, column=1)

# Book Name
label_book_name = tk.Label(root, text="Book Name:")
label_book_name.grid(row=1, column=0)
entry_book_name = tk.Entry(root)
entry_book_name.grid(row=1, column=1)

# Author Name
label_author_name = tk.Label(root, text="Author Name:")
label_author_name.grid(row=2, column=0)
entry_author_name = tk.Entry(root)
entry_author_name.grid(row=2, column=1)

# Copies Available
label_copies_available = tk.Label(root, text="Copies Available:")
label_copies_available.grid(row=3, column=0)
entry_copies_available = tk.Entry(root)
entry_copies_available.grid(row=3, column=1)

# Book Photo
label_book_photo = tk.Label(root, text="Book Photo:")
label_book_photo.grid(row=4, column=0)
label_photo = tk.Label(root)
label_photo.grid(row=4, column=1, columnspan=2)

# Retrieve button
retrieve_button = tk.Button(root, text="Retrieve Details", command=retrieve_book_details)
retrieve_button.grid(row=5, columnspan=3)

# Delete button
delete_button = tk.Button(root, text="Delete", command=delete_book_record)
delete_button.grid(row=6, columnspan=3)
delete_button.grid_remove()  # Initially, hide the delete button

# Start the Tkinter event loop
root.mainloop()
