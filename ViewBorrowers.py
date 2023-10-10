import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient
from tkinter import simpledialog
from tkinter import messagebox
from datetime import datetime
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import io

# MongoDB connection settings
MONGO_CONNECTION_STRING = "mongodb+srv://varshinisurapaneni0211:varshini1234@clusterlibrary.1vvke4p.mongodb.net/library_management_system"

DB_NAME = "library_management_system"
COLLECTION_BORROWERS = "borrowers"

def get_all_borrower_details():
    # Retrieve all borrower details from the collection
    client = MongoClient(MONGO_CONNECTION_STRING)
    db = client[DB_NAME]
    collection = db[COLLECTION_BORROWERS]
    borrower_details = list(collection.find({}))
    client.close()
    return borrower_details

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
            borrower.get("returned", "False"),
            borrower.get("returned_date_time", "")
        ))

    tree.bind("<Double-Button-1>", lambda event: on_double_click(tree))

    tree.pack(expand=True, fill="both")

    window.mainloop()

def on_double_click(tree):
    # Get the selected item's values from the Treeview widget
    selected_item = tree.selection()[0]
    values = tree.item(selected_item, "values")

    # Open a new window as a popup for editing the record
    popup = tk.Toplevel()
    popup.title("Edit Borrower Details")

    # Create labels and entry fields to display and edit the record
    labels = ["Book ID", "Book Name", "Author Name", "Borrower ID", "From Date", "To Date", "Checkout Date", "Returned", "Returned Date"]
    entries = {}
    for i, label in enumerate(labels):
        tk.Label(popup, text=label).grid(row=i, column=0)
        entry = tk.Entry(popup)
        entry.insert(tk.END, values[i])
        entry.grid(row=i, column=1)
        entries[label] = entry

    # Create date entry widgets for "From Date" and "To Date"
    from_date_picker = DateEntry(popup, date_pattern='yyyy-mm-dd')
    from_date_picker.set_date(values[4])
    from_date_picker.grid(row=4, column=1)
    to_date_picker = DateEntry(popup, date_pattern='yyyy-mm-dd')
    to_date_picker.set_date(values[5])
    to_date_picker.grid(row=5, column=1)

    # Create checkbox widget for "Returned"
    returned_var = tk.BooleanVar(value=(values[7] == "True"))
    returned_checkbox = tk.Checkbutton(popup, text="Returned", variable=returned_var)
    returned_checkbox.grid(row=7, columnspan=2)

    # Update button
    btn_update = tk.Button(popup, text="Update", command=lambda: update_record(tree, selected_item, entries, from_date_picker.get_date(), to_date_picker.get_date(), returned_var.get(), popup))
    btn_update.grid(row=len(labels), columnspan=2)

def update_record(tree, selected_item, entries, from_date, to_date, returned, popup):
    # Get the updated values from the entry fields
    updated_values = [entries[label].get() for label in entries]

    # Create a new record with the updated values
    updated_record = {
        "book_id": updated_values[0],
        "book_name": updated_values[1],
        "author_name": updated_values[2],
        "borrower_id": updated_values[3],
        "from_date_time": from_date.strftime('%Y-%m-%d'),
        "to_date_time": to_date.strftime('%Y-%m-%d'),
        "checkout_datetime": updated_values[6],
        "returned": returned,
        "returned_date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S") if returned else ""
    }

    # Update the record in the collection
    client = MongoClient(MONGO_CONNECTION_STRING)
    db = client[DB_NAME]
    collection = db[COLLECTION_BORROWERS]
    collection.update_one({"book_id": updated_values[0]}, {"$set": updated_record})
    client.close()

    # Update the Treeview widget with the new values
    tree.item(selected_item, values=updated_values)

    # Close the popup after updating
    popup.destroy()

    # Show success message
    show_update_success_popup()

    # Refresh the main window with new data
    display_borrower_details()

def show_update_success_popup():
    messagebox.showinfo("Update Success", "Record updated successfully!")

if __name__ == "__main__":
    display_borrower_details()
