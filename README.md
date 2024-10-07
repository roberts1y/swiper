# Card Swipe Tracker - Quick Setup Guide

## Overview
This project helps track entry and exit times using card swipes, with all data saved to a shared Google Sheet. If a new card is swiped, it will prompt the user to enter their UID and name.

## How to Use

### 1. Install Dependencies
Make sure you have Python installed, then run the following command to install the required libraries:
```
pip install gspread oauth2client tkinter
```

### 2. Set Up the Google Sheet
- I’ve already shared the Google Sheet with you, so no need to worry about that.
- The Google Sheet has two tabs:
  - **data**: This is where entry/exit logs go.
  - **userinf**: This is where user details like Card ID, UID, and Name are stored.

### 3. Get Your Key
Place the JSON key I gave you in the same folder as the script. Make sure it’s named `swipe-tracker-2b150ccb0439.json`.

### 4. Running the Program
- Simply run the Python script:
  ```
  python your-script-name.py
  ```
- A window will pop up where you can swipe or enter your card ID.

### 5. Swiping a Card
- **New User**: The first time you swipe, it will ask for your UID and full name.
- **Returning User**: Swipe once to log entry, then swipe again to log exit. It will show how long you stayed.

### Notes
- Make sure to keep the JSON key in the same folder as the script.
- Let me know if you run into any issues or need help!