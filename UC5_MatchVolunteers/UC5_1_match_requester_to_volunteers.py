import sqlite3
import os
import flet as ft

# ------------------------------------------
# Setup: Delete DB File if Exists
# ------------------------------------------

def setup_tables_and_sample_data():
    db_path = "cry4help.db"

    # Delete existing database to avoid schema mismatch
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create help_requests table
    cursor.execute('''
        CREATE TABLE help_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            requester_name TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            location TEXT NOT NULL,
            status TEXT DEFAULT 'open'
        )
    ''')

    # Create volunteers table
    cursor.execute('''
        CREATE TABLE volunteers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            skills TEXT NOT NULL,
            location TEXT NOT NULL
        )
    ''')

    # Sample tutoring requests
    help_requests = [
        ("Ella", "Algebra Help", "Need help with factoring equations.", "tutoring", "Room 101"),
        ("Jonathan", "Physics Tutor", "Need quick review before quiz.", "tutoring", "Library, 2nd Floor")
    ]
    cursor.executemany('''
        INSERT INTO help_requests (requester_name, title, description, category, location)
        VALUES (?, ?, ?, ?, ?)
    ''', help_requests)

    # Sample volunteers
    volunteers = [
        ("Lucas", "math,algebra,tutoring", "Room 101"),
        ("Bea", "english,reading,tutoring", "Room 204"),
        ("Carl", "physics,science,tutoring", "Library, 2nd Floor"),
        ("Jean", "python,programming,tutoring", "Library, 2nd Floor")
    ]
    cursor.executemany('''
        INSERT INTO volunteers (name, skills, location)
        VALUES (?, ?, ?)
    ''', volunteers)

    conn.commit()
    conn.close()


# ------------------------------------------
# Flet UI Preview to Confirm Setup Worked
# ------------------------------------------

def main(page: ft.Page):
    page.title = "Cry4Help - Setup Complete"
    page.window_width = 500
    page.window_height = 200
    page.bgcolor = ft.Colors.GREY_100

    setup_tables_and_sample_data()

    page.add(
        ft.Column([
            ft.Text("✅ Database recreated successfully!", size=22, weight="bold", color=ft.Colors.GREEN_700),
            ft.Text("Tables `help_requests` and `volunteers` were initialized with fresh data.", size=16)
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

ft.app(target=main)
