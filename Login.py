import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient
import subprocess

# MongoDB Atlas connection settings
MONGO_CONNECTION_STRING = "mongodb+srv://varshinisurapaneni0211:varshini1234@clusterlibrary.1vvke4p.mongodb.net/library_management_system"

DB_NAME = "library_management_system"
COLLECTION_NAME = "users"

def get_mongo_client():
    return MongoClient(MONGO_CONNECTION_STRING)

# Function to handle login button click
def login():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showwarning("Incomplete Information", "Please fill both fields.")
        return

    try:
        # Establish a connection to MongoDB
        client = get_mongo_client()
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Check if the username and password match a user record in the collection
        user = collection.find_one({"username": username, "password": password})

        if user:
            # If login is successful, close the login window and open the appropriate panel
            login_window.destroy()
            role = user.get("role")
            if role == "Manager":
                show_manager_panel()
            elif role == "User":
                show_user_panel()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

    finally:
        client.close()

# Function to close the application when the panel window is closed
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
        main_app_window.destroy()

def show_manager_panel():
    manager_panel.deiconify()

# Function to close the login window and show the user panel
def show_user_panel():
    user_panel.deiconify()

# Function to handle button clicks for manager panel
def execute_manager_action(action_number):
    # Replace with the desired actions for manager users
    if action_number == 1:
        subprocess.Popen(["python", "AddBook.py"])
    elif action_number == 2:
        subprocess.Popen(["python", "deleteBook.py"])
    elif action_number == 3:
        subprocess.Popen(["python", "viewBooks.py"])
    elif action_number == 4:
        subprocess.Popen(["python", "ViewBorrowers.py"])

# Function to handle button clicks for user panel
def execute_user_action(action_number):
    # Replace with the desired actions for regular users
    if action_number == 1:
        subprocess.Popen(["python", "ViewBooksUser.py"])
    elif action_number == 2:
        subprocess.Popen(["python", "Return.py"])

# Create the login window
login_window = tk.Tk()
login_window.title("Login")

# Username
label_username = tk.Label(login_window, text="Username:")
label_username.pack()
entry_username = tk.Entry(login_window)
entry_username.pack()

# Password
label_password = tk.Label(login_window, text="Password:")
label_password.pack()
entry_password = tk.Entry(login_window, show="*")
entry_password.pack()

# Login button
login_button = tk.Button(login_window, text="Login", command=login)
login_button.pack()

# Close the entire application if the login window is closed
login_window.protocol("WM_DELETE_WINDOW", on_closing)

# Create the main application window
main_app_window = tk.Tk()
main_app_window.title("Main Application")
main_app_window.withdraw()

# Manager Panel window
manager_panel = tk.Toplevel(main_app_window)
manager_panel.title("Manager Panel")
manager_panel.protocol("WM_DELETE_WINDOW", on_closing)
manager_panel.withdraw()

# Manager Buttons in the manager panel
manager_button1 = tk.Button(manager_panel, text="Add Book To the Libarary", command=lambda: execute_manager_action(1))
manager_button1.pack()

manager_button2 = tk.Button(manager_panel, text="Delete Book", command=lambda: execute_manager_action(2))
manager_button2.pack()

manager_button3 = tk.Button(manager_panel, text="View All Books and Update", command=lambda: execute_manager_action(3))
manager_button3.pack()

manager_button3 = tk.Button(manager_panel, text="Manage Borrowring Details", command=lambda: execute_manager_action(4))
manager_button3.pack()

# User Panel window
user_panel = tk.Toplevel(main_app_window)
user_panel.title("User Panel")
user_panel.protocol("WM_DELETE_WINDOW", on_closing)
user_panel.withdraw()

# User Buttons in the user panel
user_button1 = tk.Button(user_panel, text="View ALL Books And GET A COPY", command=lambda: execute_user_action(1))
user_button1.pack()

user_button2 = tk.Button(user_panel, text="Return Here", command=lambda: execute_user_action(2))
user_button2.pack()


# Start the Tkinter event loop
login_window.mainloop()
