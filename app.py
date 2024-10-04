import gspread
from oauth2client.service_account import ServiceAccountCredentials
import tkinter as tk
from tkinter import simpledialog, messagebox
import time

# Google Sheets setup
def setup_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('swipe-tracker-2b150ccb0439.json', scope)
    client = gspread.authorize(creds)
    return client.open("swiper").sheet1  # Replace with your Google Sheet name

# Function to log only the total time in Google Sheets
def log_time_to_google_sheet(full_name, duration):
    sheet.append_row([full_name, time.strftime('%Y-%m-%d %H:%M:%S'), f"{duration}"])
    print(f"Logged: {full_name} stayed for {duration} minutes.")

# Function to handle the card swipe
def on_card_swipe(event):
    card_id = card_input.get()  # Get card ID
    card_input.delete(0, tk.END)  # Clear input field

    # If the card ID is new, prompt for details
    if card_id not in users:
        uid = simpledialog.askstring("New User", "Enter your UID#: ")
        full_name = simpledialog.askstring("New User", "Enter your Full Name: ")
        if uid and full_name:
            users[card_id] = {"uid": uid, "name": full_name, "entry_time": None}
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

# Google Sheets
sheet = setup_google_sheets()

# Dictionary to track users and their entry/exit state
users = {}

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
