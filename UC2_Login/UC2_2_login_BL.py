import hashlib
import re
import sqlite3
import flet as ft

# ----------------------
# Validators
# ----------------------

def validate_username(username):
    return len(username) >= 5 and username.isalnum()

def validate_password(password):
    return (
        len(password) >= 8 and
        any(char.isdigit() for char in password) and
        any(char.isupper() for char in password)
    )

# ----------------------
# Login Logic
# ----------------------

def login_user(username, password, db_path="cry4help.db"):
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_pw))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# ----------------------
# Flet App UI
# ----------------------

def main(page: ft.Page):
    page.title = "Cry4Help - Login"
    page.window_width = 400
    page.window_height = 300
    page.bgcolor = ft.Colors.GREY_100

    username = ft.TextField(label="Username", width=300)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)
    message = ft.Text(value="", color=ft.Colors.RED_600)

    def handle_login(e):
        u = username.value.strip()
        p = password.value.strip()

        # Validate first
        if not validate_username(u):
            message.value = "❌ Username must be at least 5 alphanumeric characters."
        elif not validate_password(p):
            message.value = "❌ Password must be 8+ chars, 1 number & 1 uppercase."
        elif login_user(u, p):
            message.value = "✅ Login successful!"
            message.color = ft.Colors.GREEN_700
        else:
            message.value = "❌ Incorrect username or password."
            message.color = ft.Colors.RED_600

        page.update()

    login_button = ft.ElevatedButton(text="Login", on_click=handle_login, width=150)

    page.add(
        ft.Column(
            [
                ft.Text("Login to Cry4Help", size=24, weight="bold", color=ft.Colors.BLUE_900),
                username,
                password,
                login_button,
                message,
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)
