import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient

# MongoDB Atlas connection settings
MONGO_CONNECTION_STRING = "mongodb+srv://varshinisurapaneni0211:varshini1234@clusterlibrary.1vvke4p.mongodb.net/library_management_system"

DB_NAME = "library_management_system"
COLLECTION_NAME = "users"

def get_next_available_id(collection):
    # Use MongoDB's aggregate to find the maximum 'id' value in the collection
    max_id_pipeline = [
        {"$group": {"_id": None, "max_id": {"$max": {"$toInt": "$id"}}}},
        {"$project": {"_id": 0, "max_id": 1}}
    ]

    result = list(collection.aggregate(max_id_pipeline))
    next_id = 1

    if result and "max_id" in result[0]:
        next_id = int(result[0]["max_id"]) + 1

    return next_id

def get_mongo_client():
    return MongoClient(MONGO_CONNECTION_STRING)

def insert_user_record():
    user_id = entry_id.get()
    username = entry_username.get()
    password = entry_password.get()
    full_name = entry_full_name.get()
    address = entry_address.get()
    phone_number = entry_phone_number.get()
    email = entry_email.get()
    role = role_var.get()

    if not user_id or not username or not password or not full_name or not address or not phone_number or not email or not role:
        messagebox.showwarning("Incomplete Information", "Please fill all fields.")
        return

    try:
        # Convert the user_id to an integer
        user_id = int(user_id)
        print(f"User ID: {user_id}")

        # Establish a connection to MongoDB Atlas
        client = get_mongo_client()
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Create a new user record
        user_record = {
            "id": user_id,
            "username": username,
            "password": password,
            "full_name": full_name,
            "address": address,
            "phone_number": phone_number,
            "email": email,
            "role": role,
        }

        # Insert the user record into the collection
        collection.insert_one(user_record)

        # Clear the entry fields after insertion
        entry_id.delete(0, tk.END)
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        entry_full_name.delete(0, tk.END)
        entry_address.delete(0, tk.END)
        entry_phone_number.delete(0, tk.END)
        entry_email.delete(0, tk.END)

        messagebox.showinfo("Success", "User record inserted successfully.")

    except ValueError:
        messagebox.showerror("Invalid ID", "ID must be an integer.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        client.close()


# Create the main application window
root = tk.Tk()
root.title("Insert User Records")

client = get_mongo_client()
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

next_available_id = get_next_available_id(collection)
# User ID
label_id = tk.Label(root, text="ID:")
label_id.grid(row=0, column=0)
entry_id = tk.Entry(root)
entry_id.grid(row=0, column=1)
entry_id.insert(0, int(next_available_id))  # Prepopulate the ID field as a string
entry_id.config(state="readonly")

# Username
label_username = tk.Label(root, text="Username:")
label_username.grid(row=1, column=0)
entry_username = tk.Entry(root)
entry_username.grid(row=1, column=1)

# Password
label_password = tk.Label(root, text="Password:")
label_password.grid(row=2, column=0)
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=2, column=1)

# Full Name
label_full_name = tk.Label(root, text="Full Name:")
label_full_name.grid(row=3, column=0)
entry_full_name = tk.Entry(root)
entry_full_name.grid(row=3, column=1)

# Address
label_address = tk.Label(root, text="Address:")
label_address.grid(row=4, column=0)
entry_address = tk.Entry(root)
entry_address.grid(row=4, column=1)

# Phone Number
label_phone_number = tk.Label(root, text="Phone Number:")
label_phone_number.grid(row=5, column=0)
entry_phone_number = tk.Entry(root)
entry_phone_number.grid(row=5, column=1)

# Email
label_email = tk.Label(root, text="Email:")
label_email.grid(row=6, column=0)
entry_email = tk.Entry(root)
entry_email.grid(row=6, column=1)

# Role
label_role = tk.Label(root, text="Role:")
label_role.grid(row=7, column=0)
role_var = tk.StringVar(root)
role_var.set("User")  # Default role is set to "User"
role_choices = ["Manager", "User"]
role_dropdown = tk.OptionMenu(root, role_var, *role_choices)
role_dropdown.grid(row=7, column=1)

# Insert button
insert_button = tk.Button(root, text="Insert", command=insert_user_record)
insert_button.grid(row=8, columnspan=2)

# Start the Tkinter event loop
root.mainloop()
