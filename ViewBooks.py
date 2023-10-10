import tkinter as tk
from tkinter import messagebox, filedialog
from pymongo import MongoClient
from PIL import Image, ImageTk
import io

# MongoDB connection settings
MONGO_CONNECTION_STRING = "mongodb+srv://varshinisurapaneni0211:varshini1234@clusterlibrary.1vvke4p.mongodb.net/library_management_system"

DB_NAME = "library_management_system"
COLLECTION_NAME = "books"

def get_mongo_client():
    return MongoClient(MONGO_CONNECTION_STRING)

# Global variables for pagination
current_page = 1
books_per_page = 40

def get_all_books(collection):
    # Retrieve all books from the collection
    return collection.find({})

def get_books_by_author_or_title(collection, search_text, search_by):
    # Retrieve books based on author or title
    query = {"author_name": {"$regex": search_text, "$options": 'i'}} if search_by == "Author" else {"book_name": {"$regex": search_text, "$options": 'i'}}
    return collection.find(query)

def display_books(books):
    global current_page, books_per_page

    # Clear existing book display
    for widget in frame_books.winfo_children():
        widget.destroy()

    row, col = 0, 0

    for idx, book in enumerate(books, start=1):
        if idx > books_per_page:
            break

        # Book Photo
        book_photo = Image.open(io.BytesIO(book["book_photo"]))
        book_photo = book_photo.resize((100, 150))  # Resize the image if needed
        book_photo_tk = ImageTk.PhotoImage(book_photo)
        label_photo = tk.Label(frame_books, image=book_photo_tk)

        # Bind double click event to the photo label
        label_photo.bind("<Double-Button-1>", lambda event, b=book: show_book_details(b))

        label_photo.image = book_photo_tk  # Store a reference to prevent garbage collection
        label_photo.grid(row=row, column=col)

        # Book Details
        details = f"Book ID: {book['book_id']}\n" \
                  f"Book Name: {book['book_name']}\n" \
                  f"Author Name: {book['author_name']}\n" \
                  f"Copies Available: {book['copies_available']}"

        label_details = tk.Label(frame_books, text=details)
        label_details.grid(row=row + 1, column=col)

        col += 1
        if col >= 5:  # Display 5 books per row
            col = 0
            row += 2

    # Disable "Previous" button if on the first page
    btn_previous.config(state=tk.NORMAL if current_page > 1 else tk.DISABLED)

    # Disable "Next" button if there are no more books to display
    btn_next.config(state=tk.NORMAL if idx > books_per_page else tk.DISABLED)

def on_canvas_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def next_page():
    global current_page
    current_page += 1
    display_books(books_list[current_page - 1])

def previous_page():
    global current_page
    current_page -= 1
    display_books(books_list[current_page - 1])

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

def show_book_details(book):
    # Create a new Toplevel window (popup)
    popup_window = tk.Toplevel(root)
    popup_window.title("Book Details")
    popup_window.geometry("300x250")

    # Book Details
    label_book_id = tk.Label(popup_window, text="Book ID:")
    label_book_id.grid(row=0, column=0, padx=5, pady=5)
    entry_book_id = tk.Entry(popup_window, width=20, state="readonly")
    entry_book_id.grid(row=0, column=1, padx=5, pady=5)

    label_book_name = tk.Label(popup_window, text="Book Name:")
    label_book_name.grid(row=1, column=0, padx=5, pady=5)
    entry_book_name = tk.Entry(popup_window, width=20)
    entry_book_name.grid(row=1, column=1, padx=5, pady=5)

    label_author_name = tk.Label(popup_window, text="Author Name:")
    label_author_name.grid(row=2, column=0, padx=5, pady=5)
    entry_author_name = tk.Entry(popup_window, width=20)
    entry_author_name.grid(row=2, column=1, padx=5, pady=5)

    label_copies_available = tk.Label(popup_window, text="Copies Available:")
    label_copies_available.grid(row=3, column=0, padx=5, pady=5)
    entry_copies_available = tk.Entry(popup_window, width=20)
    entry_copies_available.grid(row=3, column=1, padx=5, pady=5)

    # Update button
    def update_book_details():
        # Get the updated details from the entry fields
        updated_book_name = entry_book_name.get()
        updated_author_name = entry_author_name.get()
        updated_copies_available = entry_copies_available.get()

        # Update the details in the MongoDB collection
        collection.update_one({"book_id": book["book_id"]},
                              {"$set": {"book_name": updated_book_name,
                                        "author_name": updated_author_name,
                                        "copies_available": int(updated_copies_available)}})

        # Refresh the book display after the update
        display_books(books_list[current_page - 1])

        # Close the popup window
        popup_window.destroy()

        all_books = list(get_all_books(collection))
        books_list.clear()
        for i in range(0, len(all_books), books_per_page):
            books_list.append(all_books[i:i + books_per_page])

    # Refresh the main window to update the book display
        display_books(books_list[current_page - 1])

    btn_update = tk.Button(popup_window, text="Update", command=update_book_details)
    btn_update.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

    # Prepopulate the entry fields with the book details
    entry_book_id.insert(0, book["book_id"])
    entry_book_name.insert(0, book["book_name"])
    entry_author_name.insert(0, book["author_name"])
    entry_copies_available.insert(0, book["copies_available"])

# Create the main application window
root = tk.Tk()
root.title("Books")

# Create a main frame to hold the book display and search interface
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Add a scrollbar
scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


# Add a canvas to hold the book display
canvas = tk.Canvas(main_frame, yscrollcommand=scrollbar.set)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Configure the scrollbar to scroll the canvas
scrollbar.config(command=canvas.yview)

# Create a frame inside the canvas to hold the book display
frame_books = tk.Frame(canvas)

# Add the frame_books to the canvas
canvas.create_window((0, 0), window=frame_books, anchor="nw")

# Function to handle canvas resizing and scroll region update
def on_canvas_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

# Bind the canvas to the configure event to update the scroll region
frame_books.bind("<Configure>", on_canvas_configure)

# Enable resizing of rows and columns in frame_books
for i in range(5):  # Number of columns (5 books per row)
    frame_books.columnconfigure(i, weight=1)
for i in range(40):  # Number of rows (maximum of 40 books per page)
    frame_books.rowconfigure(i, weight=1)

# Establish a connection to MongoDB
client = get_mongo_client()
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Retrieve all books and divide them into pages
all_books = list(get_all_books(collection))
books_list = [all_books[i:i + books_per_page] for i in range(0, len(all_books), books_per_page)]

# Frame to display books
#frame_books = tk.Frame(main_frame)
#frame_books.pack()

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
