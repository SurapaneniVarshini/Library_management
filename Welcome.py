import tkinter as tk
from tkinter import messagebox
import subprocess

# Function to execute the first Python program
def execute_program1():
    try:
        # Replace "python_program1.py" with the actual filename of the first Python program you want to execute
        subprocess.run(["python", "Register.py"])
    except FileNotFoundError:
        messagebox.showerror("Error", "Python program not found!")

# Function to execute the second Python program
def execute_program2():
    try:
        # Replace "python_program2.py" with the actual filename of the second Python program you want to execute
        subprocess.run(["python", "Login.py"])
    except FileNotFoundError:
        messagebox.showerror("Error", "Python program not found!")

# Create the main application window
root = tk.Tk()
root.title("Library")
root.geometry("720x600")

# Label widget for "LIBRARY"
label_library = tk.Label(root, text="LIBRARY MANAGEMENT SYSTEM", font=("Arial", 30))
label_library.pack(pady=100)

# Button widgets
btn_program1 = tk.Button(root, text="REGISTER", command=execute_program1)
btn_program1.pack(pady=40)

btn_program2 = tk.Button(root, text="LOGIN", command=execute_program2)
btn_program2.pack(pady=40)

root.mainloop()
