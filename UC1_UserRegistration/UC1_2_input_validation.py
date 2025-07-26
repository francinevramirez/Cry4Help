import flet as ft
import re

def validate_username(username):
    return len(username) >= 5 and username.isalnum()

def validate_password(password):
    return len(password) >= 8 and any(char.isdigit() for char in password) and any(char.isupper() for char in password)

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_phone(phone):
    return re.match(r"^\+?\d{10,15}$", phone)

def validate_skills(skills):
    return all(skill.strip() for skill in skills.split(","))

def main(page: ft.Page):
    page.title = "Cry4Help - Registration"
    page.window_width = 500
    page.window_height = 600
    page.scroll = ft.ScrollMode.AUTO

    username = ft.TextField(label="Username", hint_text="Min. 5 characters, letters/numbers only")
    password = ft.TextField(label="Password", password=True, can_reveal_password=True,
                            hint_text="Min. 8 chars, 1 uppercase, 1 number")
    email = ft.TextField(label="Email", hint_text="Enter a valid email address")
    phone = ft.TextField(label="Phone", hint_text="e.g. +639123456789")
    skills = ft.TextField(label="Skills", hint_text="Comma-separated e.g. tutoring, carpentry")

    result_text = ft.Text(value="", color=ft.Colors.GREEN_700)

    def register_clicked(e):
        result_text.value = ""
        # validations
        if not validate_username(username.value):
            result_text.value = "❌ Invalid username!"
        elif not validate_password(password.value):
            result_text.value = "❌ Invalid password!"
        elif not validate_email(email.value):
            result_text.value = "❌ Invalid email!"
        elif not validate_phone(phone.value):
            result_text.value = "❌ Invalid phone number!"
        elif not validate_skills(skills.value):
            result_text.value = "❌ Skills cannot be empty!"
        else:
            clean_skills = [s.strip() for s in skills.value.split(",")]
            result_text.value = f"✅ Registration successful!\nWelcome, {username.value}.\nYour skills: {clean_skills}"
            result_text.color = ft.colors.GREEN_700
        page.update()

    register_button = ft.ElevatedButton(text="Register", on_click=register_clicked)

    page.add(
        ft.Column([
            ft.Text("Cry4Help Registration", size=24, weight=ft.FontWeight.BOLD),
            username,
            password,
            email,
            phone,
            skills,
            register_button,
            result_text
        ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
    )

# Run the app
ft.app(target=main)
