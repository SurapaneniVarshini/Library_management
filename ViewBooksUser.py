import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import simpledialog
from pymongo import MongoClient
from PIL import Image, ImageTk
import io
from datetime import datetime

# MongoDB connection settings
MONGO_CONNECTION_STRING = "mongodb+srv://varshinisurapaneni0211:varshini1234@clusterlibrary.1vvke4p.mongodb.net/library_management_system"

DB_NAME = "library_management_system"
COLLECTION_NAME = "books"
COLLECTION_BORROWERS = "borrowers"

def get_mongo_client():
    return MongoClient(MONGO_CONNECTION_STRING)

# Global variables for pagination
current_page = 1
books_per_page = 40
books_per_row = 5

def previous_page():
    global current_page
    current_page -= 1
    display_books(books_list[current_page - 1])

def next_page():
    global current_page
    current_page += 1
    display_books(books_list[current_page - 1])

def get_all_books(collection):
    # Retrieve all books from the collection
    return collection.find({})

def get_books_by_author_or_title(collection, search_text, search_by):
    # Retrieve books based on author or title
    query = {"author_name": {"$regex": search_text, "$options": 'i'}} if search_by == "Author" else {"book_name": {"$regex": search_text, "$options": 'i'}}
    return collection.find(query)

def display_books(books):
    global current_page, books_per_page, books_per_row

    # Clear existing book display
    canvas.delete("all")

    row, col = 0, 0

    # Create a frame inside the canvas to hold the books
    books_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=books_frame, anchor='nw')

    for idx, book in enumerate(books, start=1):
        if idx > books_per_page:
            break

        # Book Photo
        book_photo = Image.open(io.BytesIO(book["book_photo"]))
        book_photo = book_photo.resize((100, 150))  # Resize the image if needed
        book_photo_tk = ImageTk.PhotoImage(book_photo)

        label_photo = tk.Label(books_frame, image=book_photo_tk)
        label_photo.image = book_photo_tk  # Store a reference to prevent garbage collection
        label_photo.grid(row=row, column=col)

        # Bind double-click event to the label_photo
        label_photo.bind("<Double-Button-1>", lambda event, book=book: show_book_details_popup(book))

        # Book Details
        details = f"Book ID: {book['book_id']}\n" \
                  f"Book Name: {book['book_name']}\n" \
                  f"Author Name: {book['author_name']}\n" \
                  f"Copies Available: {book['copies_available']}"

        label_details = tk.Label(books_frame, text=details)
        label_details.grid(row=row + 1, column=col)

        col += 1
        if col >= books_per_row:
            col = 0
            row += 2

    # Update the canvas scroll region
    canvas.update_idletasks()  # Update the canvas to get accurate scroll region
    canvas.config(scrollregion=canvas.bbox("all"))

    # Disable "Previous" button if on the first page
    btn_previous.config(state=tk.NORMAL if current_page > 1 else tk.DISABLED)

    # Disable "Next" button if there are no more books to display
    btn_next.config(state=tk.NORMAL if idx > books_per_page else tk.DISABLED)


try:
    from tkcalendar import DateEntry
except ImportError:
    raise ImportError("Please install 'tkcalendar' using 'pip install tkcalendar'.")

def show_book_details_popup(book):
    popup = tk.Toplevel(root)
    popup.title("Book Details")
    
    # Book Photo
    book_photo = Image.open(io.BytesIO(book["book_photo"]))
    book_photo = book_photo.resize((200, 300))  # Resize the image if needed
    book_photo_tk = ImageTk.PhotoImage(book_photo)
    
    label_photo = tk.Label(popup, image=book_photo_tk)
    label_photo.image = book_photo_tk  # Store a reference to prevent garbage collection
    label_photo.pack()

    # Book Details
    details = f"Book ID: {book['book_id']}\n" \
              f"Book Name: {book['book_name']}\n" \
              f"Author Name: {book['author_name']}\n" \
              f"Copies Available: {book['copies_available']}"

    label_details = tk.Label(popup, text=details)
    label_details.pack()
    
    label_from = tk.Label(popup, text="From Date:")
    label_from.pack()
    from_date_picker = DateEntry(popup, date_pattern='yyyy-mm-dd')
    from_date_picker.pack()

    # To Date
    label_to = tk.Label(popup, text="To Date:")
    label_to.pack()
    to_date_picker = DateEntry(popup, date_pattern='yyyy-mm-dd')
    to_date_picker.pack()

    # Checkout button
    checkout_button = tk.Button(popup, text="Checkout", command=lambda: checkout_book(book, from_date_picker.get_date(), to_date_picker.get_date(), popup))
    checkout_button.pack()

def checkout_book(book, from_date_time, to_date_time, popup):
    try:
        copies_available = int(book["copies_available"])
        if copies_available == 0:
            messagebox.showwarning("No Copies Available", "Sorry, this book is currently out of stock.")
            return

        # Update the copies_available count
        copies_available -= 1

        # Establish a connection to MongoDB
        client = get_mongo_client()
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Update the book record in the collection
        collection.update_one({"book_id": book["book_id"]}, {"$set": {"copies_available": copies_available}})
        from_date_str = from_date_time.strftime('%Y-%m-%d')
        to_date_str = to_date_time.strftime('%Y-%m-%d')
        # Insert the borrower details to the borrowers collection with default values
        borrower_details = {
            "book_id": book["book_id"],
            "book_name": book["book_name"],
            "author_name": book["author_name"],
            "borrower_id": 5,  # Replace with the actual borrower ID
            "from_date_time": from_date_str,
            "to_date_time": to_date_str,
            "checkout_datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "returned": False,  # Default value for returned field
            "returned_date_time": ""  # Default value for returned_date_time field
        }
        borrowers_collection = db[COLLECTION_BORROWERS]
        borrowers_collection.insert_one(borrower_details)

        # Close the popup after successful checkout
        popup.destroy()

        # Display updated book details after checkout
        all_books = list(get_all_books(collection))
        global books_list
        books_list = [all_books[i:i + books_per_page] for i in range(0, len(all_books), books_per_page)]
        display_books(books_list[current_page - 1])

        messagebox.showinfo("Checkout Successful", f"You have checked out {book['book_name']}.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

    finally:
        client.close()

# Create the main application window
root = tk.Tk()
root.title("Books")

# Establish a connection to MongoDB
client = get_mongo_client()
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Retrieve all books and divide them into pages
all_books = list(get_all_books(collection))
books_list = [all_books[i:i + books_per_page] for i in range(0, len(all_books), books_per_page)]

# Frame to display books with a vertical scrollbar
frame_books = tk.Frame(root)
frame_books.pack(fill=tk.BOTH, expand=True)

# Create a canvas to display books
canvas = tk.Canvas(frame_books)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar for the canvas
scrollbar = tk.Scrollbar(frame_books, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the canvas to scroll with the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)


def search_books():
    search_text = entry_search.get()
    search_by = search_var.get()
    if not search_text:
        messagebox.showwarning("Empty Search", "Please enter a search term.")
        return

    search_result = list(get_books_by_author_or_title(collection, search_text, search_by))
    count = len(search_result)
    
    if count == 0:
        messagebox.showinfo("No Results", "No books found with the specified search term.")
    else:
        books_list.clear()
        for i in range(0, count, books_per_page):
            books_list.append(search_result[i:i + books_per_page])
        global current_page
        current_page = 1
        display_books(books_list[current_page - 1])

# Search input
frame_search = tk.Frame(root)
frame_search.pack(pady=10)
entry_search = tk.Entry(frame_search, width=40)
entry_search.grid(row=0, column=0, padx=5)
search_var = tk.StringVar(root, "Author")  # Default search by "Author"
search_by_options = ["Author", "Title"]
search_option_menu = tk.OptionMenu(frame_search, search_var, *search_by_options)
search_option_menu.grid(row=0, column=1, padx=5)
btn_search = tk.Button(frame_search, text="Search", command=search_books)
btn_search.grid(row=0, column=2, padx=5)

# Pagination buttons
frame_pagination = tk.Frame(root)
frame_pagination.pack(pady=10)
btn_previous = tk.Button(frame_pagination, text="Previous", command=previous_page, state=tk.DISABLED)
btn_previous.pack(side=tk.LEFT, padx=5)
btn_next = tk.Button(frame_pagination, text="Next", command=next_page)
btn_next.pack(side=tk.LEFT, padx=5)

# Display books for the first page
display_books(books_list[current_page - 1])

# Start the Tkinter event loop
root.mainloop()
