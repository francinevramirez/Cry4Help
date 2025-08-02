# File: storematch.py

import flet as ft
import sqlite3
import os

# --- 1. Backend Database Functions ---

DB_NAME = "cry4help.db"

def setup_matches_table():
    """Creates the 'matches' table where results will be stored."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS matches (
        matchID INTEGER PRIMARY KEY AUTOINCREMENT,
        requestID INTEGER NOT NULL,
        volunteerID INTEGER NOT NULL,
        match_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (requestID) REFERENCES help_requests (id),
        FOREIGN KEY (volunteerID) REFERENCES volunteers (id)
    )
    ''')
    conn.commit()
    conn.close()

def store_match_result(request_id, volunteer_id):
    """
    THIS IS THE CORE FUNCTION FOR YOUR TASK.
    It saves the match and updates the request's status.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        # Step 1: Insert a new row into the 'matches' table to log the result.
        cursor.execute(
            "INSERT INTO matches (requestID, volunteerID) VALUES (?, ?)",
            (request_id, volunteer_id)
        )
        # Step 2: Update the original request's status to 'Matched'.
        cursor.execute(
            "UPDATE help_requests SET status = 'Matched' WHERE id = ?",
            (request_id,)
        )
        conn.commit()
        conn.close()
        return True, "✅ Match result successfully stored in the database!"
    except Exception as e:
        return False, f"❌ A database error occurred: {e}"

# --- Helper functions to get data from the DB for our UI ---
def get_open_requests():
    """Gets all help requests that currently have the status 'open'."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, category FROM help_requests WHERE status = 'open'")
    requests = cursor.fetchall()
    conn.close()
    return requests

def find_matching_volunteers(category):
    """Finds volunteers whose skills contain the request's category."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, location FROM volunteers WHERE skills LIKE ?", (f'%{category}%',))
    volunteers = cursor.fetchall()
    conn.close()
    return volunteers

# --- 2. Flet User Interface (add to the bottom of storematch.py) ---

def main(page: ft.Page):
    page.title = "Cry4Help - Store Match Result"
    page.window_width = 600
    page.window_height = 550
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Ensure the 'matches' table exists before the app starts
    setup_matches_table()

    # --- UI Controls ---
    request_dropdown = ft.Dropdown(
        label="Step 1: Select an Open Help Request",
        options=[ft.dropdown.Option(key=req[0], text=f"ID {req[0]}: {req[1]}") for req in get_open_requests()],
        width=550
    )
    volunteer_radios = ft.RadioGroup(content=ft.Text("Select a request to see matching volunteers."))
    match_button = ft.ElevatedButton("Store Match Result", disabled=True, icon=ft.icons.SAVE)
    feedback_text = ft.Text(value="", size=16)

    # --- Event Handlers ---
    def on_request_selected(e):
        """When a request is chosen, find matching volunteers."""
        selected_request_id = int(e.control.value)
        category = [req[2] for req in get_open_requests() if req[0] == selected_request_id][0]
        matching_volunteers = find_matching_volunteers(category)
        
        if matching_volunteers:
            volunteer_radios.content = ft.Column(
                [ft.Radio(value=vol[0], label=f"{vol[1]} (Location: {vol[2]})") for vol in matching_volunteers]
            )
        else:
            volunteer_radios.content = ft.Text("No volunteers found with that skill.", color=ft.colors.ORANGE)
        
        match_button.disabled = False
        page.update()

    def on_match_button_clicked(e):
        """When the match button is clicked, call the function to store the results."""
        request_id = request_dropdown.value
        volunteer_id = volunteer_radios.value

        if not request_id or not volunteer_id:
            feedback_text.value = "Error: Please select both a request and a volunteer."
            feedback_text.color = ft.colors.RED
        else:
            # THIS IS WHERE YOUR FUNCTION IS CALLED
            success, message = store_match_result(request_id, volunteer_id)
            feedback_text.value = message
            feedback_text.color = ft.colors.GREEN_700 if success else ft.colors.RED_600
            
            # Refresh the UI after a successful match
            request_dropdown.options = [ft.dropdown.Option(key=req[0], text=f"ID {req[0]}: {req[1]}") for req in get_open_requests()]
            request_dropdown.value = None
            volunteer_radios.content = ft.Text("Match stored! Select another request.")
            match_button.disabled = True

        page.update()

    # Link the functions to the controls
    request_dropdown.on_change = on_request_selected
    match_button.on_click = on_match_button_clicked

    # Add all controls to the page layout
    page.add(
        ft.Column(
            [
                ft.Text("Matchmaking System", size=28, weight="bold"),
                request_dropdown,
                ft.Divider(height=10),
                ft.Text("Step 2: Choose a Suggested Volunteer"),
                volunteer_radios,
                ft.Container(height=10),
                match_button,
                feedback_text
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

# --- 3. Entry point to run the app (add to the very bottom) ---
if __name__ == "__main__":
    ft.app(target=main)