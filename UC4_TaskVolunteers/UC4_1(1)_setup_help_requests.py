import sqlite3
import flet as ft

# -----------------------------
# DB Functions
# -----------------------------

def create_help_requests_table():
    conn = sqlite3.connect("cry4help.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS help_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            requester_name TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL CHECK (category = 'tutoring'),
            location TEXT NOT NULL,
            status TEXT DEFAULT 'open'
        )
    ''')
    conn.commit()
    conn.close()

def insert_sample_tutoring_requests():
    conn = sqlite3.connect("cry4help.db")
    cursor = conn.cursor()

    sample_data = [
        ("Ella", "Need help in Algebra", "I am struggling with factoring and quadratic equations.", "tutoring", "Room 101"),
        ("John", "Physics Review", "Looking for someone to explain Newton's Laws before the quiz.", "tutoring", "Room 204"),
        ("Mia", "Programming Basics", "Need help understanding Python loops.", "tutoring", "Library, 2nd Floor")
    ]

    cursor.executemany('''
        INSERT INTO help_requests (requester_name, title, description, category, location)
        VALUES (?, ?, ?, ?, ?)
    ''', sample_data)

    conn.commit()
    conn.close()

# -----------------------------
# Flet App to Insert & Confirm
# -----------------------------

def main(page: ft.Page):
    page.title = "Cry4Help - Seed Tutoring Requests"
    page.window_width = 500
    page.window_height = 300
    page.bgcolor = ft.Colors.GREY_100

    result_text = ft.Text(value="", size=16, color=ft.Colors.GREEN_700)

    def handle_seed(e):
        try:
            create_help_requests_table()
            insert_sample_tutoring_requests()
            result_text.value = "✅ Tutoring requests successfully inserted!"
            result_text.color = ft.Colors.GREEN_700
        except Exception as err:
            result_text.value = f"❌ Error: {err}"
            result_text.color = ft.Colors.RED_600
        page.update()

    seed_button = ft.ElevatedButton(text="Insert Sample Tutoring Requests", on_click=handle_seed)

    page.add(
        ft.Column(
            [
                ft.Text("📚 Add Tutoring Help Requests", size=24, weight="bold", color=ft.Colors.BLUE_800),
                seed_button,
                result_text
            ],
            spacing=25,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

ft.app(target=main)
