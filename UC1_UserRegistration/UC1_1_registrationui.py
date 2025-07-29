#Cry4Help Registration UI

import flet as ft
import requests

API_URL = "http://localhost:8000/register"  

def main(page: ft.Page):
    page.title = "Cry4Help"
    page.window_width = 400
    page.window_height = 600
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    name = ft.TextField(label="Full Name (LN, FN MI.)", width=350)
    email = ft.TextField(label="Email", width=350)
    password = ft.TextField(label="Password", password=True, width=350)
    skills = ft.TextField(label="Skills (comma-separated)", width=350)
    location = ft.TextField(label="Location (address or city)", width=350)
    status = ft.Text("")

    def register_user(e):
        data = {
            "name": name.value,
            "email": email.value,
            "password": password.value,
            "skills": [s.strip() for s in skills.value.split(",") if s.strip()],
            "location": location.value,
        }
        try:
            resp = requests.post(API_URL, json=data)
            if resp.status_code == 201:
                status.value = "Registration successful!"
                status.color = "green"
                name.value = email.value = password.value = skills.value = location.value = ""
            else:
                status.value = f"Error: {resp.json().get('detail', 'Unknown error')}"
                status.color = "red"
        except Exception as ex:
            status.value = f"Failed to connect to server: {ex}"
            status.color = "red"
        page.update()
    page.add(
        ft.Column([
            ft.Text("Register as Volunteer or Requester", size=20, weight="bold"),
            name,
            email,
            password,
            skills,
            location,
            ft.ElevatedButton("Register", on_click=register_user),
            status,
        ], alignment="center", horizontal_alignment="center")
    )
if __name__ == "__main__":
    ft.app(target=main)