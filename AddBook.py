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

def insert_book_record():
    book_id = entry_book_id.get()
    book_name = entry_book_name.get()
    author_name = entry_author_name.get()
    publisher = entry_publisher.get()
    price = entry_price.get()
    copies_available = entry_copies_available.get()
    description = text_description.get("1.0", tk.END).strip()

    if not book_id or not book_name or not author_name or not publisher or not price or not copies_available:
        messagebox.showwarning("Incomplete Information", "Please fill all fields.")
        return

    try:
        # Establish a connection to MongoDB
        client = get_mongo_client()
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Insert the book record into the collection
        book_record = {
            "book_id": book_id,
            "book_name": book_name,
            "author_name": author_name,
            "publisher": publisher,
            "price": price,
            "copies_available": copies_available,
            "description": description
        }

        # Check if the user has selected an image
        if image_path.get():
            with open(image_path.get(), "rb") as image_file:
                book_record["book_photo"] = image_file.read()

        collection.insert_one(book_record)

        # Clear the entry fields after insertion
        entry_book_id.delete(0, tk.END)
        entry_book_name.delete(0, tk.END)
        entry_author_name.delete(0, tk.END)
        entry_publisher.delete(0, tk.END)
        entry_price.delete(0, tk.END)
        entry_copies_available.delete(0, tk.END)
        text_description.delete("1.0", tk.END)

        # Clear the image path variable
        image_path.set("")

        messagebox.showinfo("Success", "Book record inserted successfully.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

    finally:
        client.close()

def browse_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg")])
    if file_path:
        image_path.set(file_path)

# Create the main application window
root = tk.Tk()
root.title("Add Book to Library")

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

# Publisher
label_publisher = tk.Label(root, text="Publisher:")
label_publisher.grid(row=3, column=0)
entry_publisher = tk.Entry(root)
entry_publisher.grid(row=3, column=1)

# Price
label_price = tk.Label(root, text="Price:")
label_price.grid(row=4, column=0)
entry_price = tk.Entry(root)
entry_price.grid(row=4, column=1)

# Copies Available
label_copies_available = tk.Label(root, text="Copies Available:")
label_copies_available.grid(row=5, column=0)
entry_copies_available = tk.Entry(root)
entry_copies_available.grid(row=5, column=1)

# Description
label_description = tk.Label(root, text="Description:")
label_description.grid(row=6, column=0)
text_description = tk.Text(root, height=5, width=30)
text_description.grid(row=6, column=1)

# Book Photo
label_book_photo = tk.Label(root, text="Book Photo:")
label_book_photo.grid(row=7, column=0)
image_path = tk.StringVar()
entry_book_photo = tk.Entry(root, textvariable=image_path, state="readonly")
entry_book_photo.grid(row=7, column=1)
browse_button = tk.Button(root, text="Browse", command=browse_image)
browse_button.grid(row=7, column=2)

# Register button
register_button = tk.Button(root, text="Register", command=insert_book_record)
register_button.grid(row=8, columnspan=3)

# Start the Tkinter event loop
root.mainloop()
