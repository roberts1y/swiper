import gspread
from oauth2client.service_account import ServiceAccountCredentials
import tkinter as tk
from tkinter import simpledialog, messagebox
import time
import re

# Google Sheets setup
def setup_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('swipe-tracker-2b150ccb0439.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("swiper")
    return sheet.worksheet("data"), sheet.worksheet("userinf")  # Main sheet and user info sheet

# Function to load users from the "User Info" sheet
def load_users_from_sheet(user_sheet):
    users = {}
    records = user_sheet.get_all_records()  # Get all user info records

    for record in records:
        card_id = record['Card ID']
        print(record['Card ID'])
        users[card_id] = {
            "uid": record['UID'],
            "name": record['Name'],
            "entry_time": None  # Reset entry time
        }

    return users

# Function to add a new user to the "User Info" sheet
def add_user_to_sheet(user_sheet, card_id, uid, full_name):
    user_sheet.append_row([card_id, uid, full_name])
    users[card_id] = {"uid": uid, "name": full_name, "entry_time": len(users) + 2}
    print(f"Added new user: {full_name}")

# Function to log entry/exit times
def log_time_to_google_sheet(full_name, status, duration=None):
    if status == "Entry":
        sheet.append_row([full_name, "Entered", time.strftime('%Y-%m-%d %H:%M:%S')])
    elif status == "Exit" and duration:
        sheet.append_row([full_name, "Exited", time.strftime('%Y-%m-%d %H:%M:%S'), f"Duration: {duration}"])
    print(f"Logged {status} for: {full_name}")
    
def clean_card_id(card_id):
    return re.sub(r'[^a-zA-Z0-9]', '', card_id) 
    
# Function to handle the card swipe
def on_card_swipe(event):
    raw_card_id = str(card_input.get()).strip()  # Get card ID
    card_id = clean_card_id(raw_card_id)
    card_input.delete(0, tk.END)  # Clear input field
    
    user_card_ids = set(users.keys())

    print(f"Card ID swiped: '{card_id}'")  # Debugging: Print the swiped card_id
    print(f"All loaded card IDs: {list(user_card_ids)}")  # Debugging: Print all card IDs in the users set
    # If the card ID is new, prompt for details
    if card_id not in user_card_ids:
        uid = simpledialog.askstring("New User", "Enter your UID#: ")
        full_name = simpledialog.askstring("New User", "Enter your Full Name: ")
        if uid and full_name:
            users[card_id] = {"uid": uid, "name": full_name, "entry_time": None}
            add_user_to_sheet(user_info_sheet, card_id, uid, full_name)  # Add user to sheet
            messagebox.showinfo("User Added", f"Welcome, {full_name}! You are now registered.")
    else:
        user_info = users[card_id]
        full_name = user_info["name"]

        # If the user is entering
        if user_info["entry_time"] is None:
            entry_time = time.time()
            user_info["entry_time"] = entry_time  # Store entry time
            messagebox.showinfo("Entry Recorded", f"Welcome, {full_name}! Entry recorded.")
            status_label.config(text=f"Entry recorded for {full_name}.")
        
        # If the user is exiting
        else:
            exit_time = time.time()
            entry_time = user_info["entry_time"]
            duration = round((exit_time - entry_time) / 60, 2)  # Calculate time in minutes
            user_info["entry_time"] = None  # Reset entry time
            log_time_to_google_sheet(full_name, duration)
            messagebox.showinfo("Exit Recorded", f"Goodbye, {full_name}! You stayed for {duration} minutes.")
            status_label.config(text=f"Exit recorded for {full_name}. Duration: {duration} minutes.")

# Initialize the Tkinter window
root = tk.Tk()
root.title("Card Swipe System")

# Google Sheets setup
sheet, user_info_sheet = setup_google_sheets()

# Load users from the "User Info" sheet
users = load_users_from_sheet(user_info_sheet)

# Create a label and entry for card input
tk.Label(root, text="Swipe Card:").pack(pady=10)
card_input = tk.Entry(root, width=40)
card_input.pack(padx=20, pady=5)

# Status label to display entry/exit information
status_label = tk.Label(root, text="", font=("Arial", 12), fg="green")
status_label.pack(pady=10)

# Bind the Enter key to auto-submit the data when a card is swiped
card_input.bind("<Return>", on_card_swipe)

# Run the Tkinter main loop
root.mainloop()