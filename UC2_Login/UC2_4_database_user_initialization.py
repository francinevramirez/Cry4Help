import flet as ft
import sqlite3
import hashlib
import os

DB_NAME = "cry4help.db"

# -------------------------------------------
# Database Setup for Users Table
# -------------------------------------------

def setup_users_table():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        # Insert sample users (hashed passwords)
        users = [
            ("admin", hashlib.sha256("AdminPass1".encode()).hexdigest()),
            ("jasmine", hashlib.sha256("MySecure123".encode()).hexdigest()),
            ("volunteer", hashlib.sha256("HelpMe789".encode()).hexdigest())
        ]

        cursor.executemany("INSERT INTO users (username, password) VALUES (?, ?)", users)

        conn.commit()
        conn.close()

# -------------------------------------------
# Login Validation
# -------------------------------------------

def validate_login(username, password):
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_pw))
    result = cursor.fetchone()
    conn.close()

    return result is not None

# -------------------------------------------
# Flet UI
# -------------------------------------------

def main(page: ft.Page):
    page.title = "Cry4Help - Login"
    page.window_width = 400
    page.window_height = 350
    page.bgcolor = ft.Colors.GREY_100

    setup_users_table()  # ensure table exists

    # Components
    username = ft.TextField(label="Username", width=300)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)
    status = ft.Text("", size=16)

    def handle_login(e):
        if not username.value or not password.value:
            status.value = "⚠️ Please fill in both fields."
            status.color = ft.Colors.RED_600
        elif validate_login(username.value.strip(), password.value.strip()):
            status.value = f"✅ Welcome, {username.value}!"
            status.color = ft.Colors.GREEN_700
        else:
            status.value = "❌ Invalid username or password."
            status.color = ft.Colors.RED_600
        page.update()

    # Layout
    page.add(
        ft.Column([
            ft.Text("🔐 Cry4Help Login", size=24, weight="bold", color=ft.Colors.BLUE_700),
            username,
            password,
            ft.ElevatedButton("Login", on_click=handle_login, width=300),
            status
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20)
    )

# Launch the app
ft.app(target=main)
