#Cry4Help Login UI

import flet as ft
import requests

API_URL = "http://localhost:8000/login" 

def main(page: ft.Page):
    page.title = "Cry4Help Login"
    page.window_width = 400
    page.window_height = 350
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    email = ft.TextField(label="Email", width=350)
    password = ft.TextField(label="Password", password=True, width=350)
    status = ft.Text("")

    def login_user(e):
        data = {
            "email": email.value,
            "password": password.value,
        }
        try:
            resp = requests.post(API_URL, json=data)
            if resp.status_code == 200:
                status.value = "Login successful!"
                status.color = "green"
            else:
                status.value = f"Error: {resp.json().get('detail', 'Invalid credentials')}"
                status.color = "red"
        except Exception as ex:
            status.value = f"Failed to connect to server: {ex}"
            status.color = "red"
        page.update()

    page.add(
        ft.Column([
            ft.Text("Login to Cry4Help", size=20, weight="bold"),
            email,
            password,
            ft.ElevatedButton("Login", on_click=login_user),
            status,
        ], alignment="center", horizontal_alignment="center")
    )

if __name__ == "__main__":
    ft.app(target=main)
